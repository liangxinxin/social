# coding=utf-8

from db_connect import db
import db_model_user


class UserRelation(db.Model):
    __tablename__ = 'user_relation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    relation_user_id = db.Column(db.Integer, db.ForeignKey('user.id'),unique=False)
    is_relation = db.Column(db.Boolean, unique=False)
    each_attention =db.Column(db.Boolean,unique=False,default=False)
    create_time = db.Column(db.DateTime, unique=False)
    update_time = db.Column(db.DateTime, unique=False)


    def __init__(self, user_id, relation_user_id, is_relation,each_attention, create_time, update_time):
        self.user_id = user_id
        self.relation_user_id = relation_user_id
        self.is_relation = is_relation
        self.each_attention=each_attention
        self.create_time = create_time
        self.update_time = update_time


def create_table():
    db.create_all()


def insert(user_id, relation_user_id, is_relation,create_time, update_time,each_attention=False):
    insert = UserRelation(user_id=user_id, relation_user_id=relation_user_id, is_relation=is_relation,
                          each_attention=each_attention,create_time=create_time, update_time=update_time)
    db.session.add(insert)
    db.session.commit()


def select_by_user_id(user_id, relation_user_id):
    data = UserRelation.query.filter_by(user_id=user_id, relation_user_id=relation_user_id).first()
    return data

def select_by_relation(user_id, relation_user_id,is_relation):
    data = UserRelation.query.filter_by(user_id=user_id, relation_user_id=relation_user_id,is_relation=is_relation).first()
    return data

def update(userRelation):
    row = UserRelation.query.get(userRelation.id)
    row.is_relation = userRelation.is_relation
    row.each_attention= userRelation.each_attention
    row.update_time = userRelation.update_time
    db.session.commit()


def seletct_good_friends(user_id,each_attention,page_no,num_per_page):

    paginate = UserRelation.query.filter_by(relation_user_id=user_id,each_attention=each_attention).paginate(page_no,num_per_page,False)

    return paginate


def to_json(object):
    if isinstance(object, UserRelation):
        return {
            'id': object.id,
            'user_id' : object.user_id,
            'relation_user_id' : object.relation_user_id,#被关注的人
            'is_relation':object.is_relation,
            'each_attention': object.each_attention,
            'create_time': object.create_time,
            'update_time': object.update_time,
            'user':db_model_user.to_json(object.user)
        }