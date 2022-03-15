from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
from flask import Flask, render_template, redirect, request, abort, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.posts import Post
from data.tags import Tag
from data.subscriptions import Subscription
from forms.user import RegisterForm, LoginForm, AddWorkForm
from werkzeug.datastructures import MultiDict
from sqlalchemy import or_


# from flask_restful import reqparse, abort, Api, Resource

def main():
    db_name = "db/viotag_db.sqlite"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    user1, user2 = db_sess.query(User).all()
    print(user1.subscriptions, user2.subscriptions)
    print(user1.subscribers, user2.subscribers[0].modified_date)


if __name__ == '__main__':
    main()
"""
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
