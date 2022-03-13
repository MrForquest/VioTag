from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
from flask import Flask, render_template, redirect, request, abort, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.posts import Post
from data.tags import Tag
from forms.user import RegisterForm, LoginForm, AddWorkForm
from werkzeug.datastructures import MultiDict
from sqlalchemy import or_

# from flask_restful import reqparse, abort, Api, Resource

def main():
    db_name = "db/viotag_db.sqlite"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()

    user = db_sess.query(User).first()


if __name__ == '__main__':
    main()
"""
user = User()
    user.username = "Foruqest"
    user.email = "folp22@gmail.com"
    tag = Tag(
        name="MegaTrek"
    )
    post = Post(
        text="lolkek",
        src="google"
    )
    post.tags.append(tag)
    user.posts.append(post)
    db_sess.add(user)
    db_sess.commit()
"""
