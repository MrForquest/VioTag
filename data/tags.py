import datetime
import sqlalchemy
from sqlalchemy import orm, case
from sqlalchemy.ext.hybrid import hybrid_property
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

association_table = sqlalchemy.Table(
    'post_to_tag',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('posts', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('posts.id')),
    sqlalchemy.Column('tags', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tags.id'))
)


class Tag(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tags'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    posts = orm.relation("Post", secondary="post_to_tag", back_populates="tags")

    def __repr__(self):
            return f"<Tag> {self.name}"
