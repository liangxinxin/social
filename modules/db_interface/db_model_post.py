#coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1500), unique=False)
    content = db.Column(db.Text, unique=False)
    create_user_id = db.Column(db.Integer, unique=False)
    floor_num = db.Column(db.Integer, unique=False)
    community_id = db.Column(db.Integer, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    last_update_time = db.Column(db.DateTime, unique=False)
  
    def __init__(self,title,content,create_user_id,community_id,floor_num,create_time,last_update_time):
        self.title = title
        self.content= content
        self.create_user_id = create_user_id
        self.community_id = community_id 
        self.floor_num=floor_num 
        self.create_time=create_time 
        self.last_update_time=last_update_time 

def create_table():
    db.create_all()

def insert(title,content,create_user_id,community_id,floor_num,create_time,last_update_time):
    insert=Post(title=title,content=content,create_user_id=create_user_id,community_id=community_id,floor_num=floor_num,create_time=create_time,last_update_time=last_update_time)
    db.session.add(insert)
    db.session.commit()

def select_all():
    data_all=Post.query.all()
    return data_all

def select_by_id(id):
    data=Post.query.get(id)
    return data

def update(id,title,content,create_user_id,community_id,floor_num,create_time,last_update_time):
    row = Post.query.get(id)
    row.title = title
    row.content = content
    row.create_user_id = create_user_id 
    row.community_id = community_id
    row.floor_num = floor_num
    row.create_time = create_time
    row.last_update_time = last_update_time
    db.session.commit()

def update(post):
    row = Post.query.get(post.id)
    row.title = post.title
    row.content = post.content
    row.create_user_id = post.create_user_id 
    row.community_id = post.community_id
    row.floor_num = post.floor_num
    row.create_time = post.create_time
    row.last_update_time = post.last_update_time
    db.session.commit()

def delete(id):
    data=Post.query.get(id)
    db.session.delete(data) 
    db.session.commit() 
    return data

def select_by_title(title):
    filter_string = "%" + title + "%"
    data=Post.query.filter(Post.title.like(filter_string))
    return data

def select_by_title_paging(title,page_no,num_per_page):
    filter_string = "%" + title + "%"
    paginate=Post.query.filter(Post.title.like(filter_string)).order_by(desc(Post.id)).paginate(page_no,num_per_page,False)
    return paginate

# return paginate
def select_all_paging(page_no,num_per_page,community_id):
    print 'no:',page_no,'num:',num_per_page,'commu id:',community_id
    if page_no < 1:
        page_no = 1
    paginate = Post.query.filter(Post.community_id==community_id).order_by(desc(Post.create_time)).paginate(page_no,num_per_page,False)
    print paginate
    return paginate
