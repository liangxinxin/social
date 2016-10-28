#coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
 
class UserCommunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False)
    community_id = db.Column(db.Integer, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
  
    def __init__(self,user_id,community_id,create_time):
        self.user_id = user_id
        self.community_id = community_id 
        self.create_time=create_time 

def create_table():
    db.create_all()

def insert(user_id,community_id,create_time):
    insert=UserCommunity(user_id=user_id,community_id=community_id,create_time=create_time)
    db.session.add(insert)
    db.session.commit()

def select_all():
    data_all=UserCommunity.query.all()
    return data_all

def select_by_id(id):
    data=UserCommunity.query.get(id)
    return data

def select_by_user_id_and_community_id(user_id,community_id):
    data=UserCommunity.query.filter_by(user_id=user_id,community_id=community_id).first()
    return data

def update(id,user_id,community_id,create_time):
    row = UserCommunity.query.get(id)
    row.user_id = user_id 
    row.community_id = community_id
    row.create_time = create_time
    db.session.commit()

def delete(id):
    data=UserCommunity.query.get(id)
    db.session.delete(data) 
    db.session.commit() 
    return data


# return paginate
def select_all_paging(page_no,num_per_page):
    if page_no < 1:
        page_no = 1
    paginate = UserCommunity.query.order_by(desc(UserCommunity.id)).paginate(page_no,num_per_page,False)
    return paginate
