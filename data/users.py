import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    posts = orm.relation("Post", back_populates='author')
    subscriptions = orm.relation("Subscription", primaryjoin="User.id==Subscription.subscriber_id",
                                 back_populates="subscriber")
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    subscribers = orm.relation("Subscription", primaryjoin="User.id==Subscription.publisher_id",
                               back_populates="publisher")
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tags_weights = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default=dict())
    tags_counter = sqlalchemy.Column(sqlalchemy.JSON, nullable=True, default=dict())

    def __repr__(self):
        return f"<User> {self.id} {self.username}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def update_counts(self):
        counter = dict()
        for post in self.favorite_posts:
            counter.update({tag.name: counter.get(tag.name, 0) + 1 for tag in post.tags})
        self.tags_counter = counter

    def normal_weights(self):
        if self.tags_weights == dict():
            return
        max_val = max(self.tags_weights.values())
        if max_val == 0:
            return
        self.tags_weights = {k: v / max_val for k, v in self.tags_weights.items()}
