#!/usr/bin/python
# coding=utf-8

from db_connect import db


class Action(db.Model):
    __tablename__ = 'action'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    action_type_id = db.Column(db.Integer)
    action_detail_info = db.Column(db.Text, unique=False)
    create_time = db.Column(db.DateTime, unique=False)

    def __init__(self, user_id, action_type_id, action_detail_info, create_time):
        self.user_id = user_id
        self.action_type_id = action_type_id
        self.action_detail_info = action_detail_info
        self.create_time = create_time


def create_table():
    db.create_all()


def insert(user_id, action_type_id, action_detail_info, create_time):
    action = Action(user_id=user_id, action_type_id=action_type_id, action_detail_info=action_detail_info,
                    create_time=create_time)
    db.session.add(action)
    db.session.commit()
