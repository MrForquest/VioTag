import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

likes_table = sqlalchemy.Table(
    'likes_table',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('posts', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('posts.id'))
)


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    src = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    author = orm.relation('User')
    tags = orm.relation("Tag", secondary="post_to_tag", back_populates="posts")
    comments = orm.relation('Comment', back_populates="post")
    likes = orm.relation('User', secondary="likes_table", backref="favorite_posts")

    def __repr__(self):
        return f"<Post> {self.text}"
