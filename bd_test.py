import datetime
from data import db_session
from data.users import User
from data.posts import Post
from data.tags import Tag
from data.subscriptions import Subscription
from data.comments import Comment
from sqlalchemy import or_
from string import ascii_letters
from faker import Faker
import faker
from random import randint, choice, sample
from fuzzywuzzy import process
from sqlalchemy import desc
from sqlalchemy import func

fake = Faker()

Faker.seed(1)


def generate_fake_bd():
    num_users = 20
    num_posts = 10
    num_tags = 20
    num_comments = 10
    users = list()
    tags = list()
    for i in range(num_users):
        profile = fake.simple_profile()
        user_ = User(
            email=profile["mail"],
            username=profile["username"],
            age=randint(5, 120)
        )
        user_.set_password(fake.password(length=randint(8, 30)))
        users.append(user_)

    for i in range(num_tags):
        profile = fake.simple_profile()
        tags.append(Tag(
            name=fake.word()
        ))
        user_.set_password(fake.password(length=randint(8, 30)))
        users.append(user_)

    for user_ in users:
        for j in range(num_posts + randint(-5, 5)):
            post = Post()
            post.text = fake.text(100)
            post.tags.extend(sample(tags, randint(3, 12)))
            for k in range(num_comments + randint(-5, 5)):
                com = Comment()
                com.text = fake.text(100)
                com.author = choice(users)
                post.comments.append(com)
            user_.posts.append(post)
    db_name = "db/viotag_db.sqlite"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    db_sess.add_all(users)
    db_sess.commit()


def read_bd():
    db_name = "db/viotag_db.sqlite"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    posts = db_sess.query(Post).all()
    print(len(posts[0].tags[2].posts))
    print(len(posts))


def read_bd_tags():
    name_tag = "ph"
    db_name = "db/viotag_db.sqlite"
    db_session.global_init(db_name)
    db_sess = db_session.create_session()
    posts = db_sess.query(Post, func.count(Post.id)).join(Post.tags).group_by(Post.id).all()
    tags = db_sess.query(Tag.name, func.count(Post.id)).order_by(func.count(Post.id).desc()).join(
        Tag.posts).group_by(Tag.id).all()
    stags = process.extract(name_tag, tags, limit=10)
    stags.sort(key=lambda s: (s[1], s[0][1]), reverse=True)
    print(stags)


# read_bd_tags()
generate_fake_bd()
