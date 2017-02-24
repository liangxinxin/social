# coding=utf-8
import time
from sqlalchemy import ForeignKey
from sqlalchemy import desc
from db_connect import db
import db_model_user
import db_model_reply
import db_model_post
import db_model_message_type
import db_model_comment

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
#    reply_id = db.Column(db.Integer)
    message_type_id = db.Column(db.Integer, db.ForeignKey('message_type.id'))
    user_from_id = db.Column(db.Integer)
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    has_read = db.Column(db.Boolean, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    update_time = db.Column(db.DateTime, unique=False)
    content = db.Column(db.Text)


    def __init__(self, message_type_id, user_from_id, user_to_id, post_id, reply_id,comment_id,has_read,create_time,update_time,content):
        self.message_type_id = message_type_id
        self.user_from_id = user_from_id
        self.user_to_id = user_to_id
        self.post_id = post_id 
        self.reply_id = reply_id
        self.comment_id = comment_id
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
      content= '<font color=blue><a href="http://127.0.0.1:6100/user_info?user_id='+(str)(follower_id)+\
          '" style="max-width:100px;float:left;padding-left:5px;padding-right:15px;"> ' + follower_info.name +' </a></font>' + '<p>关注了你</p>'
    print "now insert message",follower_id,followed_id,content
    content = content.encode('utf8')
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
      content= '<font color=blue><a href="http://127.0.0.1:6100/user_info?user_id='+(str)(user_from_id)+\
          '" style="max-width:100px;float:left;padding-left:5px;padding-right:10px;">' + follower_info.name+' </a></font>'\
          + '<p style="overflow: hidden;text-overflow: ellipsis;white-space:nowrap;width:15em;">\
         赞了你的回帖 <font color=blue>'+reply.content+'</font></p>'
      #content= '<font color=blue><a href="http://127.0.0.1:6100/user_info?user_id='+(str)(user_from_id)+'">' + follower_info.name +'</a> </font>' + '<p> 赞了你的回帖 </p>'
    content = content.encode('utf8')
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
      content= '<font color=blue><a href="http://127.0.0.1:6100/user_info?user_id='+(str)(user_from_id)+\
          '" style="max-width:100px;float:left;padding-left:5px;padding-right:10px;">' + follower_info.name+' </a></font>'\
          + '<p style="overflow: hidden;text-overflow: ellipsis;white-space:nowrap;width:15em;">\
         回复了你的帖 <font color=blue>'+post_info.title+'</font></p>'
    insert=Message(message_type_id=3, user_from_id=user_from_id, user_to_id=post_info.create_user_id, post_id=post_id, \
        reply_id=reply_id,has_read=False,create_time=cur_time,update_time=cur_time,content=content)
    db.session.add(insert)
    db.session.commit()


def insert_comment_reply(comment_id):
    #if no the data,insert
    comment = db_model_comment.select_by_id(comment_id)
    if comment != None:
        user = comment.user
        if user !=None:
            data=select_by_comment(3,user.id,comment.post_id,comment.reply_id,comment_id)
            if data == None:
                print 'the Message has exist !',comment.id,
                return
        else:
            print 'user is null'
            return
        ISOTIMEFORMAT='%Y-%m-%d %X'
        cur_time=time.strftime(ISOTIMEFORMAT,time.localtime())
        content = comment.content;
        insert = Message(message_type_id=3, user_from_id=comment.create_user_id, user_to_id=comment.to_user_id,
                         post_id=comment.post_id, \
                         reply_id=comment.reply_id,comment_id=comment.id, has_read=False, create_time=cur_time, update_time=cur_time, content=content)
        db.session.add(insert)
        db.session.commit()
    else:
        print 'comment is null'
        return
def select_by_message_tye_and_user_from_and_user_to(message_type_id,user_from_id, user_to_id):
    data = Message.query.filter_by(message_type_id=message_type_id,user_from_id=user_from_id, user_to_id=user_to_id).first()
    return data
def select_by_message_tye_and_user_from_and_reply_id(message_type_id,user_from_id, reply_id):
    data = Message.query.filter_by(message_type_id=message_type_id,user_from_id=user_from_id, reply_id=reply_id).first()
    return data
def select_by_message_tye_and_user_from_and_post_id_and_reply_id(message_type_id,user_from_id,post_id,reply_id):
    data = Message.query.filter_by(message_type_id=message_type_id,user_from_id=user_from_id,post_id=post_id,reply_id=reply_id).first()
    return data

def select_by_comment(message_type_id,user_from_id,post_id,reply_id,comment_id):
    data =Message.query.filter_by(message_type_id=message_type_id,user_from_id=user_from_id,post_id=post_id,reply_id=reply_id,comment_id=comment_id)
    return data


def select_by_user(user_id, page_no,num_perpage):
    paginate = Message.query.filter(Message.user_from_id==user_id).order_by(desc(Message.create_time)).paginate(page_no,num_perpage,False)
    return paginate