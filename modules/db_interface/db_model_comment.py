#coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
import db_model_user
 
class Comment(db.Model):
    __tablename__='comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=False)
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'),unique=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)
    parent_id = db.Column(db.Integer,db.ForeignKey('comment.id'),unique=False)
    reply_id = db.Column(db.Integer,db.ForeignKey('reply.id'),unique=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),unique=False)
    community_id = db.Column(db.Integer,db.ForeignKey('community.id'),unique=False)
    floor = db.Column(db.Integer, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    messages = db.relationship('Message',backref='comment',lazy='dynamic')

    def __init__(self,content,create_user_id,reply_id,to_user_id,parent_id,post_id,community_id,floor,create_time):
        self.content= content
        self.create_user_id = create_user_id
        self.reply_id = reply_id
        self.to_user_id = to_user_id
        self.parent_id = parent_id
        self.post_id =post_id
        self.community_id = community_id
        self.floor=floor 
        self.create_time=create_time 

def create_table():
    db.create_all()
def insert(content,create_user_id,reply_id,community_id,post_id,to_user_id,parent_id,floor,create_time):
    insert=Comment(content=content,create_user_id=create_user_id,reply_id=reply_id,community_id=community_id,post_id=post_id,to_user_id=to_user_id,parent_id=parent_id,floor=floor,create_time=create_time)
    db.session.add(insert)
    db.session.commit()
    return insert

def select_all():
    data_all=Comment.query.all()
    return data_all

def select_by_reply_id(reply_id,page_no,num_per_page):
    paginate=Comment.query.filter(Comment.reply_id==reply_id).order_by(desc(Comment.create_time)).paginate(page_no,num_per_page,False)
    return paginate

def select_by_id(id):
    data=Comment.query.get(id)
    return data

def delete(id):
    data=Comment.query.get(id)
    db.session.delete(data) 
    db.session.commit() 
    return data


# return paginate
def select_all_paging(page_no,num_per_page):
    if page_no < 1:
        page_no = 1
    paginate = Comment.query.order_by(desc(Comment.id)).paginate(page_no,num_per_page,False)
    return paginate

def to_json(object):
    if isinstance(object, Comment):
        return {
            'id': object.id,
            'content': object.content,
            'create_user_id': object.create_user_id,
            'reply_id':object.reply_id,
            'parent_id':object.parent_id,
            'floor':object.floor,
            'create_time':object.create_time,
            'user':db_model_user.to_json(object.user),
            'touser':db_model_user.to_json(object.touser)

        }