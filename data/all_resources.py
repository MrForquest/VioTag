from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.posts import Post
from data.comments import Comment
from data.tags import Tag
from flask import jsonify
import sqlite3


def abort_if_not_found(idd, thing):
    session = db_session.create_session()
    news = session.query(Post).get(idd)
    if not news:
        abort(404, message=f"{thing} {idd} not found")


class Post_resource(Resource):
    def get(self, post_id):
        abort_if_not_found(post_id, 'Post')
        session = db_session.create_session()
        post = session.query(Post).get(post_id)
        return jsonify({'post': post.to_dict()})


class Post_list_resource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Post).all()
        return jsonify({'posts': [item.to_dict() for item in news]})


class Post_comments_resource(Resource):
    def get(self, post_id):
        abort_if_not_found(post_id, 'Post')
        session = db_session.create_session()
        post = session.query(Post).get(post_id)
        return jsonify({'comments': post.to_dict(only=('comments'))})


class Comment_resource(Resource):
    def get(self, comm_id):
        abort_if_not_found(comm_id, 'Comment')
        session = db_session.create_session()
        comm = session.query(Comment).get(comm_id)
        return jsonify({'comment': comm.to_dict()})


class Tag_post_resource(Resource):
    def get(self, tag_id):
        conn = sqlite3.connect('db/viotag_db.sqlite')
        cur = conn.cursor()
        session = db_session.create_session()
        abort_if_not_found(tag_id, 'Tag_post')
        posts = cur.execute(f"""SELECT posts FROM post_to_tag WHERE tags = {tag_id}""").fetchall()
        answ = [i[0] for i in posts]
        ret = session.query(Post).get(*answ)
        return jsonify({'posts': [item.to_dict() for item in ret]})
