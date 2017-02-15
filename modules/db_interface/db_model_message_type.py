# coding=utf-8

from db_connect import db


class MessageType(db.Model):
    __tablename__ = 'message_type'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.String(1500))
    #messages=db.relationship('Message',backref='message_type',lazy='dynamic')

    def __init__(self, content):
        self.content = content


def create_table():
    db.create_all()

