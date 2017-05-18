# coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
import db_model_user
import db_model_comment
from modules.Logger import *


class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.LargeBinary, unique=False)
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), unique=False)
    floor = db.Column(db.Integer, unique=False)
    floor_num = db.Column(db.Integer, unique=False)
    like_num = db.Column(db.Integer, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    status = db.Column(db.Boolean, unique=False, default=0)
    last_update_time = db.Column(db.DateTime, unique=False)
    messages = db.relationship('Message', backref='reply', lazy='dynamic')
    comments = db.relationship('Comment', backref='reply', lazy='dynamic')

    def __init__(self, content, create_user_id, post_id, floor, floor_num, like_num, create_time, status,
                 last_update_time):
        self.content = content
        self.create_user_id = create_user_id
        self.post_id = post_id
        self.floor = floor
        self.floor_num = floor_num
        self.like_num = like_num
        self.create_time = create_time
        self.status = status
        self.last_update_time = last_update_time


def create_table():
    db.create_all()


def insert(content, create_user_id, post_id, floor, floor_num, like_num, create_time, status, last_update_time):
    insert_data = Reply(content=content, create_user_id=create_user_id, post_id=post_id, floor=floor,
                        floor_num=floor_num, like_num=like_num, create_time=create_time, status=status,
                        last_update_time=last_update_time)
    db.session.add(insert_data)
    db.session.commit()
    return insert_data


def select_all():
    data_all = Reply.query.filter_by(status=0).all()
    return data_all


def select_by_id(id):
    data = Reply.query.get(id)
    return data


def select_by_create_user_and_post_and_floor(create_user_id, post_id, floor):
    data = Reply.query.filter_by(create_user_id=create_user_id, post_id=post_id, floor=floor, status=0).first()
    return data


def update(id, content, create_user_id, post_id, floor, floor_num, like_num, create_time, status, last_update_time):
    row = Reply.query.get(id)
    row.content = content
    row.create_user_id = create_user_id
    row.post_id = post_id
    row.floor = floor
    row.floor_num = floor_num
    row.like_num = like_num
    row.create_time = create_time
    row.status = status
    row.last_update_time = last_update_time
    db.session.commit()


def update(reply):
    row = Reply.query.get(reply.id)
    row.content = reply.content
    row.status = reply.status
    row.last_update_time = reply.last_update_time
    db.session.commit()


def delete(id):
    data = Reply.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return data


def select_paging_by_post_id(page_no, num_per_page, post_id):
    Logger.infoLogger.info('no:%s,num:%s,post id:%s',page_no,num_per_page,post_id)
    paginate = Reply.query.filter(Reply.post_id == post_id, Reply.status == 0).order_by(Reply.create_time).paginate(
        page_no, num_per_page, False)
    return paginate


def select_except_best_id(page_no, num_per_page, post_id, best_reply_id):
    Logger.infoLogger.info('no:%s','num:%s,post id:%s',page_no,num_per_page,post_id)
    paginate = Reply.query.filter(Reply.post_id == post_id, Reply.status == 0, Reply.id != best_reply_id).order_by(
        Reply.create_time).paginate(page_no, num_per_page, False)
    return paginate


def select_best_by_post_id(post_id):
    Logger.infoLogger.info('post id:%s', post_id)
    best_reply = Reply.query.filter(Reply.post_id == post_id, Reply.status == 0, Reply.like_num >= 3).order_by(
        desc(Reply.like_num)).first()
    return best_reply


# return paginate
def select_all_paging(page_no, num_per_page):
    if page_no < 1:
        page_no = 1
    paginate = Reply.query.filter_by(status=0).order_by(desc(Reply.id)).paginate(page_no, num_per_page, False)
    return paginate


def update_floor_num(id, floor_num):
    row = Reply.query.get(id)
    row.floor_num = floor_num
    db.session.commit()


def update_like_num(id, like_num, last_update_time):
    row = Reply.query.get(id)
    row.like_num = like_num
    row.last_update_time = last_update_time
    db.session.commit()


def to_json(object):
    if isinstance(object, Reply):
        return {
            'id': object.id,
            'content': object.content,
            'create_user_id': object.create_user_id,
            'post_id': object.post_id,
            'floor': object.floor,
            'floor_num': object.floor_num,
            'like_num': object.like_num,
            'create_time': object.create_time,
            'status': object.status,
            'last_update_time': object.last_update_time,
            'user': db_model_user.to_json(object.user),
            'comments': db_model_comment.to_json(object.comments)

        }
