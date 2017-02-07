# coding=utf-8

from db_connect import db


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    message_type_id = db.Column(db.Integer, db.ForeignKey('message_type.id'))
    user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'))
    has_read = db.Column(db.Boolean, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    update_time = db.Column(db.DateTime, unique=False)


    def __init__(self, message_type_id, user_from_id, user_to_id, post_id, reply_id,has_read,create_time,update_time):
        self.message_type_id = message_type_id
        self.user_from_id = user_from_id
        self.user_to_id = user_to_id
        self.post_id = post_id 
        self.reply_id = reply_id
        self.has_read = has_read
        self.create_time = create_time
        self.update_time = update_time


def create_table():
    db.create_all()

