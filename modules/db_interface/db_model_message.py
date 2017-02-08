# coding=utf-8
import time
from sqlalchemy import ForeignKey
from db_connect import db
import db_model_user
import db_model_reply
import db_model_post
import db_model_message_type
import db_model_message_type

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
#    reply_id = db.Column(db.Integer)
    message_type_id = db.Column(db.Integer, db.ForeignKey('message_type.id'))
    user_from_id = db.Column(db.Integer)
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'))
    has_read = db.Column(db.Boolean, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    update_time = db.Column(db.DateTime, unique=False)
    content = db.Column(db.Text)


    def __init__(self, message_type_id, user_from_id, user_to_id, post_id, reply_id,has_read,create_time,update_time,content):
        self.message_type_id = message_type_id
        self.user_from_id = user_from_id
        self.user_to_id = user_to_id
        self.post_id = post_id 
        self.reply_id = reply_id
        self.has_read = has_read
        self.create_time = create_time
        self.update_time = update_time
        self.content = content


def create_table():
    db.create_all()

def insert_follow(follower_id,followed_id):
    #if no the data,insert
    data=select_by_message_tye_and_user_from_and_user_to(1,follower_id, followed_id)
    if data != None:
      print " the follow relation have exist",follower_id, followed_id
      return
    ISOTIMEFORMAT='%Y-%m-%d %X'
    cur_time=time.strftime(ISOTIMEFORMAT,time.localtime())
    content = ""
    follower_info = db_model_user.select_by_id(follower_id)
    if follower_info != None:
      content= '<a href=http://127.0.0.1:6100/user_info?user_id=>'+(str)(follower_id) + follower_info.name +'</a>' + '关注了你'
    print "now insert message",follower_id,followed_id,content
    insert=Message(message_type_id=1, user_from_id=(int)(follower_id), user_to_id=(int)(followed_id), post_id= None,\
        reply_id=None,has_read=False,create_time=cur_time,update_time=cur_time,content=content)
    db.session.add(insert)
    db.session.commit()

def insert_praise_reply(user_from_id,reply_id):
    #if no the data,insert
    data=select_by_message_tye_and_user_from_and_reply_id(2,user_from_id, reply_id)
    if data != None:
      print " the message have exist",user_from_id, reply_id
      return
    reply=db_model_reply.select_by_id(reply_id) 
    ISOTIMEFORMAT='%Y-%m-%d %X'
    cur_time=time.strftime(ISOTIMEFORMAT,time.localtime())
    content = ""
    follower_info = db_model_user.select_by_id(user_from_id)
    if follower_info != None and reply != None:
      content= '<a href=http://127.0.0.1:6100/user_info?user_id=>'+(str)(user_from_id) + follower_info.name +'</a>' + '赞了你的回帖' + reply.content
    insert=Message(message_type_id=2, user_from_id=user_from_id, user_to_id=reply.create_user_id, post_id=reply.post_id,\
        reply_id=reply_id,has_read=False,create_time=cur_time,update_time=cur_time,content=content)
    db.session.add(insert)
    db.session.commit()

def insert_reply_post(user_from_id,post_id,reply_id):
    #if no the data,insert
    data=select_by_message_tye_and_user_from_and_post_id_and_reply_id(3,user_from_id,post_id,reply_id)
    if data != None:
      print " the message have exist",user_from_id,post_id,reply_id
      return
    post_info = db_model_post.select_by_id(post_id)
    if post_info == None:
      print "error message param,post id is invalid",post_id
      return
    ISOTIMEFORMAT='%Y-%m-%d %X'
    cur_time=time.strftime(ISOTIMEFORMAT,time.localtime())
    content = ""
    follower_info = db_model_user.select_by_id(user_from_id)
    if follower_info != None:
      content= '<a href=http://127.0.0.1:6100/user_info?user_id=>'+(str)(user_from_id) + follower_info.name +'</a>'\
         + '在帖子 ' + post_info.content + ' 回复了你'
    insert=Message(message_type_id=3, user_from_id=user_from_id, user_to_id=post_info.create_user_id, post_id=post_id, \
        reply_id=reply_id,has_read=False,create_time=cur_time,update_time=cur_time,content=content)
    db.session.add(insert)
    db.session.commit()

def select_by_message_tye_and_user_from_and_user_to(message_type_id,user_from_id, user_to_id):
    data = Message.query.filter_by(message_type_id=message_type_id,user_from_id=user_from_id, user_to_id=user_to_id).first()
    return data
def select_by_message_tye_and_user_from_and_reply_id(message_type_id,user_from_id, reply_id):
    data = Message.query.filter_by(message_type_id=message_type_id,user_from_id=user_from_id, reply_id=reply_id).first()
    return data
def select_by_message_tye_and_user_from_and_post_id_and_reply_id(message_type_id,user_from_id,post_id,reply_id):
    data = Message.query.filter_by(message_type_id=message_type_id,user_from_id=user_from_id,post_id=post_id,reply_id=reply_id).first()
    return data
