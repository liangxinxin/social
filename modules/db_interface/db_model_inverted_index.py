# -*- coding:utf-8 -*-
from db_connect import db


class InvertedIndex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True)
    post_id = db.Column(db.String(500), unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    last_update_time = db.Column(db.DateTime, unique=False)

    def __init__(self, word, post_id, create_time, last_update_time):
        self.word = word
        self.post_id = post_id
        self.create_time = create_time
        self.last_update_time = last_update_time


def create_table():
    db.create_all()


def select_by_post_id(post_id):
    filter_string = "%s%s%s" % ('%', str(int(post_id)),'%')
    data = InvertedIndex.query.filter(InvertedIndex.post_id.like(filter_string)).all()
    return data


def select_by_word(word):
    data = InvertedIndex.query.filter_by(word=word).first()
    return data


def insert(word, post_id, create_time, last_update_time):
    insert = InvertedIndex(word=word, post_id=post_id, create_time=create_time, last_update_time=last_update_time)
    db.session.add(insert)
    db.session.commit()
    return insert


def update(object):
    row = InvertedIndex.query.get(object.id)
    row.post_id = object.post_id
    row.last_update_time = object.last_update_time
    db.session.commit()


def to_json(obejct):
    if isinstance(obejct, InvertedIndex):
        return {
            'id': obejct.id,
            'word': obejct.word,
            'post_id': obejct.post_id,
            'create_time': obejct.create_time,
            'last_update_time': obejct.last_update_time
        }
