# coding=utf-8
import time

from sqlalchemy import desc

import db_model_comment
import db_model_post
import db_model_reply
import db_model_user
from db_connect import db


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    message_type_id = db.Column(db.Integer, db.ForeignKey('message_type.id'))
    user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    has_read = db.Column(db.Boolean, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    update_time = db.Column(db.DateTime, unique=False)
    content = db.Column(db.Text)

    def __init__(self, message_type_id, user_from_id, user_to_id, post_id, reply_id, comment_id, has_read, create_time,
                 update_time, content):
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


def select_by_id(id):
    return Message.query.get(id)


def insert_comment_message(user_from_id, user_to_id, comment_id):
    # if no the data, insert
    message_type_id = 4
    data = select_comment_message(message_type_id, user_from_id, user_to_id, comment_id)
    if data:
        print " the message have exist", user_from_id, comment_id
        return
    comment = db_model_comment.select_by_id(comment_id)
    if comment:
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        cur_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        content = comment.user.name + '回复了我' + comment.content
        insert = Message(message_type_id=message_type_id, user_from_id=comment.create_user_id, user_to_id=comment.to_user_id,
                         post_id=comment.post_id,reply_id=comment.reply_id, comment_id=comment.id, has_read=False,
                         create_time=cur_time,update_time=cur_time, content=content)
        db.session.add(insert)
        db.session.commit()
    else:
        print 'comment is null'


def update_has_read(id, has_read):
    data = select_by_id(id)
    if data:
        data.has_read = int(has_read)
        db.session.commit()


def insert_follow(follower_id, followed_id):  #guanzhu
    # if non-existent，insert
    message_type_id = 1
    data = select_follwer_message(message_type_id, follower_id, followed_id)
    if data:
        print ' the follow relation have exist', follower_id, followed_id
        return
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    cur_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    content = ''
    follower_info = db_model_user.select_by_id(follower_id)
    if follower_info:
        content = follower_info.name + '关注了我。'
    print 'now insert message', follower_id, followed_id, content
    content = content.encode('utf8')
    insert = Message(message_type_id=1, user_from_id=(int)(follower_id), user_to_id=(int)(followed_id), post_id=None,
                     reply_id=None, comment_id=None, has_read=False, create_time=cur_time, update_time=cur_time,
                     content=content)
    db.session.add(insert)
    db.session.commit()


def insert_zan_reply(user_from_id, reply_id):
    # if non-existent，insert
    message_type_id = 2
    data = select_zan_message(message_type_id, user_from_id, reply_id)
    if data:
        print ' the message have exist', user_from_id, reply_id
        return
    reply = db_model_reply.select_by_id(reply_id)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    cur_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    content = ''
    follower_info = db_model_user.select_by_id(user_from_id)
    if follower_info and reply:
        content = follower_info.name + '赞了我的评论。'
    content = content.encode('utf8')
    insert = Message(message_type_id=message_type_id, user_from_id=user_from_id, user_to_id=reply.create_user_id,
                     post_id=reply.post_id, reply_id=reply_id, comment_id=None, has_read=False,
                     create_time=cur_time, update_time=cur_time, content=content)
    db.session.add(insert)
    db.session.commit()


def insert_reply_post(user_from_id, post_id, reply_id):
    # if  non-existent, insert
    message_type_id = 3
    data = select_reply_to_post(message_type_id, user_from_id, post_id, reply_id)
    if data:
        print " the message have exist", user_from_id, post_id, reply_id
        return
    post_info = db_model_post.select_by_id(post_id)
    reply = db_model_reply.select_by_id(reply_id)
    if post_info:
        print ' error message param,post id is invalid', post_id
        return
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    cur_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    content = ''
    follower_info = db_model_user.select_by_id(user_from_id)
    if follower_info and reply:
        content = follower_info.name + '评论了我' + reply.content
    insert = Message(message_type_id=message_type_id, user_from_id=user_from_id, user_to_id=post_info.create_user_id, post_id=post_id, \
                     reply_id=reply_id, comment_id=None, has_read=False, create_time=cur_time, update_time=cur_time,
                     content=content)
    db.session.add(insert)
    db.session.commit()



def select_follwer_message(message_type_id, user_from_id, user_to_id):  # query guanzhu
    data = Message.query.filter_by(message_type_id=message_type_id, user_from_id=user_from_id,
                                   user_to_id=user_to_id).first()
    return data


def select_zan_message(message_type_id, user_from_id, reply_id):
    data = Message.query.filter_by(message_type_id=message_type_id, user_from_id=user_from_id,
                                   reply_id=reply_id).first()
    return data


def select_reply_to_post(message_type_id, user_from_id, post_id, reply_id):
    data = Message.query.filter_by(message_type_id=message_type_id, user_from_id=user_from_id, post_id=post_id,
                                   reply_id=reply_id).first()
    return data


def select_comment_message(message_type_id, user_from_id, user_to_id, comment_id):
    data = Message.query.filter_by(message_type_id=message_type_id, user_from_id=user_from_id, user_to_id=user_to_id,
                                       comment_id=comment_id).first()
    return data


def select_total_by_type_user(message_type_id, user_to_id):
    count = Message.query.filter_by(message_type_id=message_type_id, user_to_id=user_to_id).count()
    return count


def select_message_by_to_user(message_type_id, user_to_id, page_no, num_perpage):
    unread_list = []
    if page_no == 1:
        unread_list = Message.query.filter_by(message_type_id=message_type_id, user_to_id=user_to_id,
                                              has_read=False).order_by(desc(Message.create_time)).all()
    read_list = Message.query.filter_by(message_type_id=message_type_id, user_to_id=user_to_id, has_read=True).order_by(
        desc(Message.create_time)).paginate(page_no, num_perpage, False)
    return read_list, unread_list


def select_num_unread_by_type(has_read, user_id):
    count_comment = Message.query.filter_by(message_type_id=4, has_read=has_read, user_to_id=user_id).count()
    count_reply = Message.query.filter_by(message_type_id=3, has_read=has_read, user_to_id=user_id).count()
    count_guanzhu = Message.query.filter_by(message_type_id=1, has_read=has_read, user_to_id=user_id).count()
    count_do_good = Message.query.filter_by(message_type_id=2, has_read=has_read, user_to_id=user_id).count()
    return count_comment, count_reply, count_guanzhu, count_do_good
