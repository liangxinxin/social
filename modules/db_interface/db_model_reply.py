#coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
import  db_model_user
 
class Reply(db.Model):
    __tablename__='reply'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=False)
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'),unique=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),unique=False)
    floor = db.Column(db.Integer, unique=False)
    floor_num = db.Column(db.Integer, unique=False)
    like_num= db.Column(db.Integer, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    messages = db.relationship('Message',backref='reply',lazy='dynamic')
    comments= db.relationship('Comment',backref='reply',lazy='dynamic')

    def __init__(self,content,create_user_id,post_id,floor,floor_num,like_num,create_time):
        self.content= content
        self.create_user_id = create_user_id
        self.post_id = post_id 
        self.floor=floor
        self.floor_num=floor_num
        self.like_num =like_num
        self.create_time=create_time 

def create_table():
    db.create_all()

def insert(content,create_user_id,post_id,floor,floor_num,like_num,create_time):
    insert=Reply(content=content,create_user_id=create_user_id,post_id=post_id,floor=floor,floor_num=floor_num,like_num=like_num,create_time=create_time)
    db.session.add(insert)
    db.session.commit()

def select_all():
    data_all=Reply.query.all()
    return data_all

def select_by_id(id):
    data=Reply.query.get(id)
    return data

def select_by_create_user_and_post_and_floor(create_user_id,post_id,floor):
    data=Reply.query.filter_by(create_user_id=create_user_id,post_id=post_id,floor=floor).first()
    return data

def update(id,content,create_user_id,post_id,floor,floor_num,like_num,create_time):
    row = Reply.query.get(id)
    row.content = content
    row.create_user_id = create_user_id 
    row.post_id = post_id
    row.floor = floor
    row.floor_num = floor_num
    row.like_num = like_num
    row.create_time = create_time
    db.session.commit()

def delete(id):
    data=Reply.query.get(id)
    db.session.delete(data) 
    db.session.commit() 
    return data

def select_paging_by_post_id(page_no,num_per_page,post_id):
    print 'no:',page_no,'num:',num_per_page,'post id:',post_id
    if page_no < 1:
        page_no = 1
    paginate = Reply.query.filter(Reply.post_id==post_id).order_by(desc(Reply.create_time)).paginate(page_no,num_per_page,False)
    return paginate

# return paginate
def select_all_paging(page_no,num_per_page):
    if page_no < 1:
        page_no = 1
    paginate = Reply.query.order_by(desc(Reply.id)).paginate(page_no,num_per_page,False)
    return paginate


def update_floor_num(id,floor_num):
    row = Reply.query.get(id)
    row.floor_num = floor_num
    db.session.commit()

def update_like_num(id,like_num):
    row = Reply.query.get(id)
    row.like_num = like_num
    db.session.commit()

def to_json(object):
    if isinstance(object, Reply):
        return {
            'id':object.id,
            'content': object.content,
            'create_user_id':object.create_user_id,
            'post_id':object.post_id,
            'floor':object.floor,
            'floor_num':object.floor_num,
            'like_num':object.like_num,
            'create_time':object.create_time,
            'user':db_model_user.to_json(object.user)

        }