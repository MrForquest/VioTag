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
from forms.post import AddPostForm, SearchForm
from sqlalchemy import or_
from flask_restful import reqparse, abort, Api, Resource
from data.all_resources import *
from sqlalchemy import or_, func, desc
from fuzzywuzzy import fuzz, process
import logging
import os
from data.utilits import get_rmd_posts, update_all_weights

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
    filename='viotag.log'
)
logger = logging.getLogger(__name__)
MAX_FILE_SIZE = 1024 * 1024 * 10 + 1

application = Flask(__name__)
application.config['SECRET_KEY'] = 'werty57i39fj92udifkdb56fwed232z'
application.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
login_manager = LoginManager()
login_manager.init_app(application)
api = Api(application)
api.add_resource(Post_resource, '/api/v1/post/<int:post_id>')
api.add_resource(Post_list_resource, '/api/v1/posts')
api.add_resource(Post_comments_resource, '/api/v1/comments_post/<int:post_id>')
api.add_resource(Comment_resource, '/api/v1/comment/<int:comm_id>')
api.add_resource(Tag_post_resource, '/api/v1/tag/<int:tag_id>')
db_name = "db/viotag_db.sqlite"
db_session.global_init(db_name)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@application.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache,no-store,max-age=0'
    return response


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(121)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@application.route('/register', methods=['GET', 'POST'])
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


@application.route('/relevant_tags', methods=['GET'])
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


@application.route('/addpost', methods=['GET', 'POST'])
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
        return redirect(f"/profile/{current_user.username}.html")
    return render_template('add_post.html', form=form)


@application.route('/', methods=['GET'])
@login_required
def index():
    db_sess = db_session.create_session()
    recommendations = list(map(lambda p: p[0], get_recommend_posts(30)))
    posts = db_sess.query(Post).filter(Post.id.in_(recommendations)).all()
    for p in posts:
        p.num_likes = len(p.likes)
    user = db_sess.query(User).get(current_user.id)
    data = dict()
    data["title"] = "Главная"
    data["posts"] = posts
    data["author_id"] = user.id
    data["posts_like_id"] = list(map(lambda u: u.id, user.favorite_posts))
    # print(data["posts_like_id"])
    return render_template('index.html', **data)


@application.route('/profile/<username>.html', methods=['GET', 'POST'])
def profile(username):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    data = dict()
    if user.id == current_user.id:
        data["title"] = "Мой профиль"
    else:
        data["title"] = f"Профиль {username}"
    data["about"] = user.about if user.about else ""
    if user.avatar is None:
        data["avatar"] = "../static/images/default_avatar.jpg"
    else:
        data["avatar"] = "../" + user.avatar
    data["username"] = user.username
    data["num_subscribers"] = len(user.subscribers)
    sub = db_sess.query(Subscription).filter(Subscription.subscriber_id == current_user.id,
                                             Subscription.publisher_id == user.id).first()
    user_curr = db_sess.query(User).get(current_user.id)
    data["u1su2"] = not bool(sub)
    posts = db_sess.query(Post).filter(Post.author_id == user.id).order_by(
        desc(Post.modified_date)).all()
    for p in posts:
        p.num_likes = len(p.likes)
    data["posts"] = posts
    data["author_id"] = user.id
    data["posts_like_id"] = list(map(lambda u: u.id, user_curr.favorite_posts))

    return render_template('user_profile.html', **data)


@application.route("/avatar_upload", methods=['POST'])
def avatar_upload():
    file = request.files["avatar_upload"]
    db_sess = db_session.create_session()
    if file.filename:
        if bool(file.filename):
            file_bytes = file.read()
            additional = file.filename.split(".")[-1]
            store_name = f"{current_user.id}_{-1}_1.{additional}"
            if store_name in os.listdir("static/store/"):
                os.remove(f"static/store/{store_name}")
                store_name = f"{current_user.id}_{-2}_1.{additional}"
            path = f"static/store/{store_name}"
            file_sv = open(path, "wb")
            file_sv.write(file_bytes)
            file_sv.close()
            file.close()
            current_user.avatar = path
            user = db_sess.query(User).get(current_user.id)
            user.avatar = path
            db_sess.commit()
        else:
            print("error")
            return jsonify({"success": False})
    return jsonify({"success": True})


@application.route("/subscribe_user", methods=['POST'])
def subscribe_upload():
    db_sess = db_session.create_session()
    author_id = int(request.form.get("user_id"))
    author = db_sess.query(User).get(author_id)
    sub = db_sess.query(Subscription).filter(Subscription.subscriber_id == current_user.id,
                                             Subscription.publisher_id == author_id).first()
    if sub:
        print("delete")
        db_sess.delete(sub)
        db_sess.commit()
        return jsonify({"success": True, "subscribe": False})
    else:
        print("add")
        sub = Subscription(subscriber_id=current_user.id, publisher_id=author_id)
        db_sess.add(sub)
        db_sess.commit()
        return jsonify({"success": True, "subscribe": True})


@application.route("/btn_like_click", methods=['POST'])
def btn_like_click():
    db_sess = db_session.create_session()
    like_btn_id = request.form.get("like_btn_id")
    post_id = int(like_btn_id.split("_")[2])
    post = db_sess.query(Post).get(post_id)
    data = dict()
    data["success"] = True
    user = db_sess.query(User).get(current_user.id)
    if post.id in map(lambda u: u.id, user.favorite_posts):
        post.likes.remove(user)
        data["like"] = False
    else:
        print("like")
        post.likes.append(user)
        data["like"] = True
    db_sess.commit()
    return jsonify(data)


def get_recommend_posts(num):
    update_all_weights()
    posts_id = get_rmd_posts(current_user.id, num)
    return posts_id


@application.route('/welcome', methods=['GET', 'POST'])
def welcome():
    db_sess = db_session.create_session()
    data = dict()
    data["title"] = "Добро пожаловать!"
    return render_template('welcome.html', **data)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/welcome")


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/welcome")


@application.route("/view_post", methods=['POST'])
def view_post_checker():
    db_sess = db_session.create_session()
    post_id_viewed = request.form.get("post_id_viewed")
    post_id = int(post_id_viewed.split("_")[1])
    post = db_sess.query(Post).get(post_id)
    user = db_sess.query(User).get(current_user.id)
    if not (post in user.viewed):
        user.viewed.append(post)
    db_sess.commit()

    data = dict()
    data["success"] = True
    return jsonify(data)


@application.route('/search', methods=['GET', 'POST'])
def search_post():
    form = SearchForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        text = form.text.data.lower()
        tags_names = set(form.tags.data.split(";"))
        posts = db_sess.query(Post).all()
        res = list()
        print(tags_names)
        if tags_names != {''}:
            for post in posts:
                tags = set(map(lambda t: t.name, post.tags))
                if tags_names <= tags:
                    res.append(post)
        if not res and tags_names != {''}:
            res = list()
        else:
            res = res if res else posts

        if text:
            res = sorted(
                map(lambda p: (
                fuzz.partial_ratio(p.author.username.lower() + " " + p.text.lower(), text.lower()),
                p),
                    res), reverse=True, key=lambda s: s[0])[:200]
            res = list(map(lambda p: p[1], res))
        for p in res:
            p.num_likes = len(p.likes)
        user = db_sess.query(User).get(current_user.id)
        data = dict()
        data["title"] = "Поиск"
        data["posts"] = res
        data["author_id"] = user.id
        data["posts_like_id"] = list(map(lambda u: u.id, user.favorite_posts))
        return render_template('search.html', **data, form=form)

    return render_template('search.html', form=form)


@application.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    subr = [s.publisher.id for s in user.subscriptions]
    print(subr)
    posts = db_sess.query(Post).filter(Post.author_id.in_(subr)).order_by(
        desc(Post.modified_date)).all()
    for p in posts:
        p.num_likes = len(p.likes)
    data = dict()
    data["title"] = "Подписки"
    data["posts"] = posts
    data["posts_like_id"] = list(map(lambda u: u.id, user.favorite_posts))
    return render_template('subs.html', **data)


def main():
    application.run(port=5000)


if __name__ == '__main__':
    main()
