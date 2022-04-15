from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
from flask import Flask, render_template, redirect, request, abort, jsonify, make_response
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.posts import Post
from data.tags import Tag
from data.subscriptions import Subscription
from data.comments import Comment
from forms.user import RegisterForm, LoginForm
from forms.post import AddPostForm
from werkzeug.datastructures import MultiDict
from sqlalchemy import or_
from flask_restful import reqparse, abort, Api, Resource
from data.all_resources import *
from sqlalchemy import or_, func, desc
from fuzzywuzzy import process

MAX_FILE_SIZE = 1024 * 1024 * 10 + 1

app = Flask(__name__)
app.config['SECRET_KEY'] = 'werty57i39fj92udifkdb56fwed232z'
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(Post_resource, '/api/v1/post/<int:post_id>')
api.add_resource(Post_list_resource, '/api/v1/posts')
api.add_resource(Post_comments_resource, '/api/v1/comments_post/<int:post_id>')
api.add_resource(Comment_resource, '/api/v1/comment/<int:comment_id>')
api.add_resource(Tag_post_resource, '/api/v1/tag/<int:tag_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Это имя пользователя уже занято")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с такой электронной почтой уже есть")
        if form.age.data < 4:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Чтобы зарегистрироваться вам должно быть минимум 5 лет.")
        user = User(
            username=form.username.data,
            email=form.email.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/relevant_tags', methods=['GET'])
def relevant_tags():
    if request.method == 'GET':
        name_tag = request.args.get("name_tag")

        db_sess = db_session.create_session()
        tags = db_sess.query(Tag.name, func.count(Post.id)).order_by(
            func.count(Post.id).desc()).join(
            Tag.posts).group_by(Tag.id).all()
        posts = db_sess.query(Post.id).order_by(func.count(Post.id).desc()).join(
            Tag.posts).group_by(Tag.id).all()
        stags = process.extract(name_tag, tags, limit=4)
        stags.sort(key=lambda s: (s[1], s[0][1]), reverse=True)

        return jsonify(
            list(map(lambda s: {"tag": [{"name": s[0][0]}, {"rs": [s[1], s[0][1]]}]}, stags)))


@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        tags_names = form.tags.data.split(";")
        tags = list()
        for name in tags_names:
            tag = db_sess.query(Tag).filter(Tag.name == name).first()
            if not tag:
                tag = Tag(name=name)
            tags.append(tag)
        text = form.text.data
        img_fg = False
        file = request.files["img"]
        if bool(file.filename):
            file_bytes = file.read()
            if len(file_bytes) < MAX_FILE_SIZE:
                img_fg = True
            else:
                print("error")

        post = Post(text=text, author_id=current_user.id)
        post.tags.extend(tags)
        db_sess.add(post)
        db_sess.commit()

        if img_fg:
            additional = file.filename.split(".")[-1]
            path = f"static/store/{post.author.id}_{post.id}_1.{additional}"
            file_sv = open(path, "wb")
            file_sv.write(file_bytes)
            file_sv.close()
            db_sess.commit()
            post.src = path
        db_sess.commit()
        return redirect("/profile")
    return render_template('add_post.html', form=form)


@app.route('/', methods=['GET'])
def index():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(1)
    login_user(user, remember=True)
    return render_template('index.html', title="Главная")


@app.route('/profile/<username>.html', methods=['GET', 'POST'])
def profile(username):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(2)
    login_user(user, remember=True)
    user = db_sess.query(User).filter(User.username == username).first()
    data = dict()
    data["title"] = "Мой профиль"
    data["about"] = user.about if user.about else ""
    if user.avatar is None:
        data["avatar"] = "../static/images/default_avatar.jpg"
    else:
        data["avatar"] = "../" + user.avatar
    data["username"] = user.username
    sub = db_sess.query(Subscription).filter(Subscription.subscriber_id == current_user.id,
                                             Subscription.publisher_id == user.id).first()
    data["u1su2"] = bool(sub)
    posts = db_sess.query(Post).filter(Post.author_id == user.id).order_by(
        desc(Post.modified_date)).all()
    data["posts"] = posts
    data["author_id"] = user.id
    return render_template('user_profile.html', **data)


@app.route("/avatar_upload", methods=['POST'])
def avatar_upload():
    file = request.files["avatar_upload"]
    db_sess = db_session.create_session()
    if file.filename:
        if bool(file.filename):
            file_bytes = file.read()
            additional = file.filename.split(".")[-1]
            path = f"static/store/{current_user.id}_{-1}_1.{additional}"
            file_sv = open(path, "wb")
            file_sv.write(file_bytes)
            file_sv.close()
            current_user.avatar = path
            rows_changed = db_sess.query(User).filter_by(username=current_user.username).update(
                dict(avatar=path))
            db_sess.commit()
        else:
            print("error")
    return jsonify({"success": True})


@app.route("/subscribe_user", methods=['POST'])
def subscribe_upload():
    db_sess = db_session.create_session()
    author_id = int(request.form.get("user_id"))
    author = db_sess.query(User).get(author_id)
    print(current_user.id, author_id)
    sub = db_sess.query(Subscription).filter(Subscription.subscriber_id == current_user.id,
                                             Subscription.publisher_id == author_id).first()
    print(author_id, sub)
    if sub:
        print("delete")
        db_sess.delete(sub)
        db_sess.commit()
        return jsonify({"success": True, "subscribe": False})
    else:
        print("add")
        sub = Subscription(subscriber_id=current_user.id, publisher_id=author_id)
        # author.subscribers.append(sub)
        # current_user.subscriptions.append(sub)
        # rows_changed = db_sess.query(User).filter_by(id=current_user.id).update(
        #   dict(subscriptions=current_user.subscriptions))
        db_sess.add(sub)
        db_sess.commit()
        return jsonify({"success": True, "subscribe": True})


def main():
    db_name = "db/viotag_db.sqlite"
    db_session.global_init(db_name)
    app.run(port=5000)


if __name__ == '__main__':
    main()
