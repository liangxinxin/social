# coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db


class DefaultImage(db.Model):
    __tablename__ = 'default_image'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(2), unique=False)
    imgsrc = db.Column(db.String(100), unique=False)

    def __init__(self, imgsrc, type):
        self.type = type
        self.imgsrc = imgsrc


def create_table():
    db.create_all()


def select_by_type(typeid, page_no, num_per_page):
    paginate = DefaultImage.query.filter_by(type=typeid).paginate(page_no, num_per_page, False)
    return paginate


def to_json(object):
    if isinstance(object, DefaultImage):
        return {
            'id': object.id,
            'type': object.type,
            'imgsrc': object.imgsrc
        }
