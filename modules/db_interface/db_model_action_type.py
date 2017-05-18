#!/usr/bin/python
# coding=utf-8

from db_connect import db
from modules.Logger import *


class ActionType(db.Model):
    __tablename__ = 'action_type'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.String(250))

    def __init__(self, content):
        self.content = content


def create_table():
    db.create_all()


def insert_default_value():
    insert = ActionType(content='注册')
    db.session.add(insert)
    db.session.commit()
    
    insert2 = ActionType(content='登录')
    db.session.add(insert2)
    db.session.commit()

    insert3 = ActionType(content='发帖')
    db.session.add(insert3)
    db.session.commit()

    insert4 = ActionType(content='回帖')
    db.session.add(insert4)
    db.session.commit()

    insert5 = ActionType(content='回复')
    db.session.add(insert5)
    db.session.commit()

    insert6 = ActionType(content='回帖点赞')
    db.session.add(insert6)
    db.session.commit()

    insert7 = ActionType(content='发帖点赞')
    db.session.add(insert7)
    db.session.commit()

    insert8 = ActionType(content='发私信')
    db.session.add(insert8)
    db.session.commit()

    insert9 = ActionType(content='关注')
    db.session.add(insert9)
    db.session.commit()

    insert10 = ActionType(content='取关')
    db.session.add(insert10)
    db.session.commit()

    insert11 = ActionType(content='创建社区')
    db.session.add(insert11)
    db.session.commit()

    insert12 = ActionType(content='加入社区')
    db.session.add(insert12)
    db.session.commit()

    insert13 = ActionType(content='离开社区')
    db.session.add(insert13)
    db.session.commit()


def get_type_id(action_name):
    name_id_dict = {'regist' : 1, 'login': 2, 'create_post': 3,'reply_post': 4, 'comment': 5,'praise_reply': 6,
                    'praise_post': 7, 'create_private_message': 8, 'follow': 9,'cancel_follow': 10,
                    'create_community': 11, 'join_community': 12, 'left_community': 13}
    result = 0
    try:
        result=name_id_dict[action_name]
    except Exception,e:
        print e
        Logger.infoLogger.error('Exception:%s',e)
    return result
