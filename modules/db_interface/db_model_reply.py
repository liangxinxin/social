#coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
 
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=False)
    create_user_id = db.Column(db.Integer, unique=False)
    post_id = db.Column(db.Integer, unique=False)
    floor = db.Column(db.Integer, unique=False)
    create_time = db.Column(db.Datetime, unique=False)
  
    def __init__(self, id,content,create_user_id,post_id,floor,create_time):
        self.id = id 
        self.content= content
        self.create_user_id = create_user_id
        self.post_id = post_id 
        self.floor=floor 
        self.create_time=create_time 

def create_table():
    db.create_all()

def insert(content,create_user_id,post_id,floor,create_time):
    insert=Reply(content=content,create_user_id=create_user_id,post_id=post_id,floor=floor,create_time=create_time)
    db.session.add(insert)
    db.session.commit()

def select_all():
    data_all=Reply.query.all()
    return data_all

def select_by_id(id):
    data=Reply.query.get(id)
    return data

def update(id,content,create_user_id,post_id,floor,create_time):
    row = Reply.query.get(id)
    row.content = content
    row.create_user_id = create_user_id 
    row.post_id = post_id
    row.floor = floor
    row.create_time = create_time
    db.session.commit()

def delete(id):
    data=Reply.query.get(id)
    db.session.delete(data) 
    db.session.commit() 
    return data


# return paginate
def select_all_paging(page_no,num_per_page):
    if page_no < 1:
        page_no = 1
    paginate = Reply.query.order_by(desc(Reply.id)).paginate(page_no,num_per_page,False)
    return paginate
