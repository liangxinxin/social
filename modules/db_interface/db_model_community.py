#coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
 
class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False)
    describe = db.Column(db.String(500), unique=False)
    head_img_url = db.Column(db.String(500), unique=False)
    user_num = db.Column(db.Integer, unique=False)
    post_num = db.Column(db.Integer, unique=False)
    create_user_id = db.Column(db.Integer, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    last_update_time = db.Column(db.DateTime, unique=False)
  
    def __init__(self,name,user_num,post_num,describe,head_img_url,create_user_id,create_time):
        self.name = name
        self.user_num = user_num
        self.post_num = post_num 
        self.describe= describe
        self.head_img_url=head_img_url 
        self.create_user_id=create_user_id 
        self.create_time=create_time 

def create_table():
    db.create_all()

def insert(name,user_num,post_num,describe,head_img_url,create_user_id,create_time):
    insert=Community(name=name,user_num=user_num,post_num=post_num,describe=describe,head_img_url=head_img_url,create_user_id=create_user_id,create_time=create_time)
    db.session.add(insert)
    db.session.commit()

def select_all():
    data_all=Community.query.all()
    return data_all

def select_by_id(id):
    data=Community.query.get(id)
    return data

def update(id,name,user_num,post_num,describe,head_img_url,create_user_id,create_time):
    row = Community.query.get(id)
    row.name = name
    row.user_num = user_num 
    row.post_num = post_num
    row.describe = describe
    row.head_img_url = head_img_url
    row.create_user_id = create_user_id
    row.create_time = create_time
    db.session.commit()

def update(community):
    row = Community.query.get(community.id)
    row.name = community.name
    row.user_num = community.user_num 
    row.post_num = community.post_num
    row.describe = community.describe
    row.head_img_url = community.head_img_url
    row.create_user_id = community.create_user_id
    row.create_time = community.create_time
    db.session.commit()

def delete(id):
    data=Community.query.get(id)
    db.session.delete(data) 
    db.session.commit() 
    return data

def select_by_name_like(name):
    filter_string = "%" + name + "%"
    data=Community.query.filter(Community.name.like(filter_string))
    return data

def select_by_name_equal(name):
    data=Community.query.filter(Community.name==name).first()
    return data

def select_by_name_paging(name,page_no,num_perpage):
    filter_string = "%" + name + "%"
    paginate=Community.query.filter(Community.name.like(filter_string)).order_by(desc(Community.post_num)).paginate(page_no,num_perpage,False)
    return paginate

# return paginate
def select_all_paging(page_no,num_perpage):
    if page_no < 1:
        page_no = 1
    paginate = Community.query.order_by(desc(Community.id)).paginate(page_no,num_perpage,False)
    return paginate

