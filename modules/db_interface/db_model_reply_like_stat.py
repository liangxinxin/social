#coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
 
class ReplyLikeActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reply_id = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
  
    def __init__(self,reply_id,user_id,create_time):
        self.reply_id= reply_id
        self.user_id = user_id
        self.create_time=create_time 

def create_table():
    db.create_all()

def is_reply_liked_by_user(reply_id, user_id):
    print "is_reply_liked_by_user:", reply_id, user_id
    count=ReplyLikeActivity.query.filter_by(reply_id=reply_id, user_id=user_id).count()
    return count > 0

def get_reply_like_count(reply_id):
    return ReplyLikeActivity.query.filter(ReplyLikeActivity.reply_id==reply_id).count()

def insert(reply_id, user_id, create_time):
    insert=ReplyLikeActivity(reply_id=reply_id, user_id=user_id, create_time=create_time)
    db.session.add(insert)
    db.session.commit()

def remove(reply_id, user_id):
    data=ReplyLikeActivity.query.filter_by(reply_id=reply_id, user_id=user_id).first()
    db.session.delete(data) 
    db.session.commit()


def like_user(id,page_no,num_per_page):
    data = ReplyLikeActivity.query.filter_by(reply_id=id).order_by(desc(ReplyLikeActivity.create_time)).paginate(page_no,num_per_page,False)
    return data

