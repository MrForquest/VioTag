import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Subscription(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subscriptions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    payment = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    subscriber_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    publisher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    subscriber = orm.relation('User', foreign_keys="Subscription.subscriber_id")
    publisher = orm.relation('User', foreign_keys="Subscription.publisher_id")

    def __repr__(self):
        return f"<Subscription> {self.subscriber} to {self.publisher}"
