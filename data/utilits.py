from sklearn.decomposition import NMF
import numpy as np
from data import db_session
from data.users import User
from data.posts import Post
from data.tags import Tag


def update_all_weights():
    db_sess = db_session.create_session()
    us = db_sess.query(User).all()
    users = {u.id: u for u in us}
    uis = map(lambda u: u.id, us)

    tags = set()
    for u in us:
        u.update_counts()
        tags.update(u.tags_counter)

    tags = sorted(tags)
    uis = sorted(uis)
    matrix = np.array([[0] * len(uis)])
    for y in range(len(tags)):
        x = np.array([list(map(lambda s: us[s].tags_counter.get(tags[y], 0), range(len(uis))))])
        matrix = np.concatenate((matrix, x))
    matrix = np.delete(matrix, 0, 0)

    model = NMF(n_components=3, init='nndsvd', random_state=0)
    w = model.fit_transform(matrix)
    h = model.components_
    narr = np.round(np.dot(w, h), 2)

    for j in range(len(uis)):
        weights = narr[:, j]
        dict_weights = dict(zip(tags, weights))
        dict_weights = dict((k, v) for k, v in dict_weights.items() if v)
        users[uis[j]].tags_weights = dict_weights
        users[uis[j]].normal_weights()
    db_sess.commit()


def get_rmd_posts(user_id, num):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    update_all_weights()
    posts = db_sess.query(Post).filter(Post.id.not_in(map(lambda u: u.id, user.viewed))).all()
    post_ratings = list()
    for post in posts:
        tags_post = set(map(lambda t: t.name, post.tags))
        rating = sum([user.tags_weights.get(i, 0) for i in tags_post])
        post_ratings.append((post.id, rating))
    post_ratings.sort(key=lambda s: s[1], reverse=True)
    return post_ratings[:num]
