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
        return jsonify({'post': post.to_dict(only=('tags.name', "tags.id", 'text', 'author_id'))})


class Post_list_resource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Post).all()
        return jsonify({'posts': [item.to_dict(only=('tags.name', "tags.id", 'text', 'author_id')) for item in news]})


class Post_comments_resource(Resource):
    def get(self, post_id):
        abort_if_not_found(post_id, 'Post')
        session = db_session.create_session()
        post = session.query(Post).get(post_id)
        return jsonify({'comments': post.to_dict(only=('tags.name', "tags.id", 'text', 'author_id'))})


class Comment_resource(Resource):
    def get(self, comm_id):
        abort_if_not_found(comm_id, 'Comment')
        session = db_session.create_session()
        comm = session.query(Comment).get(comm_id)
        return jsonify({'comment': comm.to_dict(only=('modified_date', "author_id", 'text', 'post_id'))})


class Tag_post_resource(Resource):
    def get(self, tag_id):
        session = db_session.create_session()
        abort_if_not_found(tag_id, 'Tag_post')
        ret = session.query(Tag).get(tag_id).posts
        return jsonify({'posts': [item.to_dict(only=('tags.name', "tags.id", 'text', 'author_id')) for item in ret]})
