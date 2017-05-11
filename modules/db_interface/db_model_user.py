# coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False)
    password = db.Column(db.String(150), unique=False)
    age = db.Column(db.Integer, unique=False)
    sex = db.Column(db.Integer, unique=False)
    mobile = db.Column(db.String(15), unique=False)
    email = db.Column(db.String(100), unique=False)
    professional = db.Column(db.String(300), unique=False)
    head_img_url = db.Column(db.String(500), unique=False)
    location = db.Column(db.String(150), unique=False)
    post_num = db.Column(db.Integer, unique=False, default=0)
    by_attention_num = db.Column(db.Integer, unique=False, default=0)
    attention_num = db.Column(db.Integer, unique=False, default=0)
    label = db.Column(db.String(300), unique=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    relations = db.relationship('UserRelation', backref='user', lazy='dynamic', foreign_keys='UserRelation.user_id')
    messages = db.relationship('Message', backref='user', lazy='dynamic', foreign_keys='Message.user_from_id')
    to_user_messages = db.relationship('Message', backref='touser', lazy='dynamic', foreign_keys='Message.user_to_id')
    comments = db.relationship('Comment', backref='user', lazy='dynamic', foreign_keys='Comment.create_user_id')
    to_user_comments = db.relationship('Comment', backref='touser', lazy='dynamic', foreign_keys='Comment.to_user_id')
    replys = db.relationship('Reply', backref='user', lazy='dynamic')
    private_mess_user = db.relationship('PrivateMessage', backref='user', lazy='dynamic',
                                        foreign_keys='PrivateMessage.create_user_id')
    private_mess_to_user = db.relationship('PrivateMessage', backref='touser', lazy='dynamic',
                                           foreign_keys='PrivateMessage.to_user_id')

    def __init__(self, name, password, mobile, age, sex, email, professional, head_img_url, location, label, post_num,
                 attention_num, by_attention_num):
        self.name = name
        self.password = password
        self.age = age
        self.sex = sex
        self.mobile = mobile
        self.email = email
        self.professional = professional
        self.head_img_url = head_img_url
        self.location = location
        self.label = label
        self.post_num = post_num
        self.by_attention_num = by_attention_num
        self.attention_num = attention_num


def create_table():
    db.create_all()


def insert(name, password, mobile, age=0, sex=2, email="", professional="",
           head_img_url="https://img3.doubanio.com/icon/g232413-3.jpg", location="", label="", post_num=0,
           attention_num=0, by_attention_num=0):
    insert = User(name=name, password=password, age=age, sex=sex, mobile=mobile, email=email, professional=professional,
                  head_img_url=head_img_url, location=location, label=label, post_num=post_num,
                  attention_num=attention_num, by_attention_num=by_attention_num)
    db.session.add(insert)
    db.session.commit()


def select_all():
    data_all = User.query.all()
    return data_all


def select_by_id(id):
    data = User.query.get(id)
    return data


def select_full_match_by_name(name):
    data = User.query.filter_by(name=name).first()
    return data


def select_by_name_and_password(name, password):
    data = User.query.filter_by(name=name, password=password).first()
    return data


def select_by_mobile_and_password(mobile, password):
    data = User.query.filter_by(mobile=mobile, password=password).first()
    return data


def select_by_name_and_password_and_mobile(name, password, mobile):
    data = User.query.filter_by(name=name, password=password, mobile=mobile).first()
    return data


def select_by_mobile(mobile):
    data = User.query.filter_by(mobile=mobile).first()
    return data


def update(id, name, password, mobile, age, sex, email, professional, head_img_url, location, label):
    row = User.query.get(id)
    row.name = name
    row.password = password
    row.age = age
    row.sex = sex
    row.mobile = mobile
    row.email = email
    row.professional = professional
    row.head_img_url = head_img_url
    row.location = location
    row.label = label
    db.session.commit()


def update_user(user):
    row = User.query.get(user.id)
    row.post_num = user.post_num
    row.by_attention_num = user.by_attention_num
    row.attention_num = user.attention_num
    db.session.commit()


def update_user(user):
    update(user.id, user.name, user.password, user.mobile, user.age, user.sex, user.email, \
           user.professional, user.head_img_url, user.location, user.label)


def delete(id):
    data = User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return data


def select_by_name(name):
    filter_string = "%" + name + "%"
    data = User.query.filter(User.name.like(filter_string))
    return data


def select_by_name_paging(name, page_no, num_per_page):
    filter_string = "%" + name + "%"
    paginate = User.query.filter(User.name.like(filter_string)).order_by(desc(User.id)).paginate(page_no, num_per_page,
                                                                                                 False)
    return paginate


# return paginate
def select_all_paging(page_no, num_per_page):
    if page_no < 1:
        page_no = 1
    paginate = User.query.order_by(desc(User.id)).paginate(page_no, num_per_page, False)
    return paginate


def save_head_image(id, imageUrl):
    row = User.query.get(id)
    row.head_img_url = imageUrl
    db.session.commit()


def to_json(object):
    if isinstance(object, User):
        return {
            'id': object.id,
            'name': object.name,
            'head_img_url': object.head_img_url,
            'post_num': object.post_num,
            'by_attention_num': object.by_attention_num,
            'attention_num': object.attention_num,
            'professional': object.professional
        }
