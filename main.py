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
from forms.user import RegisterForm, LoginForm
from forms.post import AddPostForm
from werkzeug.datastructures import MultiDict
from sqlalchemy import or_
from flask_restful import reqparse, abort, Api, Resource
from data.all_resources import *
from sqlalchemy import or_, func
from fuzzywuzzy import process

app = Flask(__name__)
app.config['SECRET_KEY'] = 'werty57i39fj92udifkdb56fwed232z'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(Post_resource, '/api/v1/post/<int:post_id>')
api.add_resource(Post_list_resource, '/api/v1/posts')
api.add_resource(Post_comments_resource, '/api/v1/comments_post/<int:post_id>')
api.add_resource(Comment_resource, '/api/v1/comment/<int:comment_id>')
api.add_resource(Tag_post_resource, '/api/v1/tag/<int:tag_id>')


# from flask_restful import reqparse, abort, Api, Resource
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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
        print(name_tag)
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
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        print(form.tags.data)

    return render_template('add_post.html', form=form)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def main():
    db_name = "db/viotag_db.sqlite"
    db_session.global_init(db_name)
    app.run()


if __name__ == '__main__':
    main()
"""
    print(user1.posts[0].comments.append(Comment(text="cat good",
                                                 author=user1)))
    print(user1.posts[0].comments[0])
    print(user1.subscriptions, user2.subscriptions)
    print(user1.subscribers, user2.subscribers[0].modified_date)

  user1, user2 = db_sess.query(User).all()
    user1.subscriptions.append(Subscription(subscriber=user1,
                                            publisher=user2))
    db_sess.commit()
        user = User()
    user.username = "Fool"
    user.email = "folp11@gmail.com"
    tag = Tag(
        name="Mega2Trek"
    )
    post = Post(
        text="lolkek23",
        src="google"
    )
    post.tags.append(tag)
    user.posts.append(post)
    db_sess.add(user)
    db_sess.commit()
        user1, user2 = db_sess.query(User).all()
    user1.subscriptions.append(user2)
    print(user1, user1.subscriptions)
    print(user2, user2.subscriptions)
    user1.subscriptions.remove(user2)
    db_sess.commit()
"""
"""
def main():
    db_name = "db/viotag_db.sqlite"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    user1, user2 = db_sess.query(User).all()
    posts = db_sess.query(Post).all()
    print(user2.posts[0].author_id)
    print(posts[0].comments)
    print(posts[0].tags)
    db_sess.commit()
    """
