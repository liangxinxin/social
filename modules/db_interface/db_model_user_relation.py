# coding=utf-8

from db_connect import db


class UserRelation(db.Model):
    __tablename__ = 'user_relation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    relation_user_id = db.Column(db.Integer, unique=False)
    is_relation = db.Column(db.Integer, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    update_time = db.Column(db.DateTime, unique=False)


    def __init__(self, user_id, relation_user_id, is_relation, create_time, update_time):
        self.user_id = user_id
        self.relation_user_id = relation_user_id
        self.is_relation = is_relation
        self.create_time = create_time
        self.update_time = update_time


def create_table():
    db.create_all()


def insert(user_id, relation_user_id, is_relation, create_time, update_time):
    data = UserRelation.query.filter_by(user_id=user_id, relation_user_id=relation_user_id).first()

    insert = UserRelation(user_id=user_id, relation_user_id=relation_user_id, is_relation=is_relation,
                          create_time=create_time, update_time=update_time)
    db.session.add(insert)
    db.session.commit()


def select_by_user_id(user_id, relation_user_id):
    data = UserRelation.query.filter_by(user_id=user_id, relation_user_id=relation_user_id).first()
    return data


def update(user_id, relation_user_id, is_relation,update_time):
    row = select_by_user_id(user_id, relation_user_id)
    row.is_relation = is_relation
    row.update_time = update_time
    db.session.commit()
