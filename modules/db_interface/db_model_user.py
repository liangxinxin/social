#coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
 
class User(db.Model):
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
  
    def __init__(self, id,name,age,sex,mobile,email,professional,head_img_url,location):
        self.id = id 
        self.name = name
        self.age = age
        self.sex = sex 
        self.mobile= mobile
        self.email=email 
        self.professional=professional 
        self.head_img_url=head_img_url 
        self.location=location 

def create_table():
    db.create_all()

def insert(name,age,sex,mobile,email,professional,head_img_url,location):
    insert=User(name=name,age=age,sex=sex,mobile=mobile,email=email,professional=professional,head_img_url=head_img_url,location=location)
    db.session.add(insert)
    db.session.commit()

def select_all():
    data_all=User.query.all()
    return data_all

def select_by_id(id):
    data=User.query.get(id)
    return data

def select_by_name_and_password(name,password):
    data=User.query.filter_by(name=name,password=password).first()
    return data

def update(id,name,age,sex,mobile,email,professional,head_img_url,location):
    row = User.query.get(id)
    row.name = name
    row.age = age 
    row.sex = sex
    row.mobile = mobile
    row.email = email
    row.professional = professional
    row.head_img_url = head_img_url
    row.location = location
    db.session.commit()

def delete(id):
    data=User.query.get(id)
    db.session.delete(data) 
    db.session.commit() 
    return data

def select_by_name(name):
    filter_string = "%" + name + "%"
    data=User.query.filter(User.name.like(filter_string))
    return data

def select_by_name_paging(name,page_no,num_per_page):
    filter_string = "%" + name + "%"
    paginate=User.query.filter(User.name.like(filter_string)).order_by(desc(User.id)).paginate(page_no,num_per_page,False)
    return paginate

# return paginate
def select_all_paging(page_no,num_per_page):
    if page_no < 1:
        page_no = 1
    paginate = User.query.order_by(desc(User.id)).paginate(page_no,num_per_page,False)
    return paginate
