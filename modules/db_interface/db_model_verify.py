#coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
 
class Verify(db.Model):
    __tablename__='verify'
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(15), unique=False)
    sms_code = db.Column(db.String(10), unique=False)

    def __init__(self,mobile,sms_code):
        self.mobile = mobile
        self.sms_code = sms_code

def create_table():
    db.create_all()

def insert(mobile,sms_code):
    insert=Verify(mobile=mobile,sms_code=sms_code)
    db.session.add(insert)
    db.session.commit()

def select_by_id(id):
    data=Verify.query.get(id)
    return data

def select_by_mobile(mobile):
    data=Verify.query.filter_by(mobile=mobile).first()
    return data

def select_by_mobile_and_sms_code(mobile,sms_code):
    data=Verify.query.filter_by(mobile=mobile,sms_code=sms_code).first()
    return data

