# coding=utf-8
from sqlalchemy import desc, asc, or_, and_

import db_model_user
from db_connect import db


class PrivateMessage(db.Model):
    __tablename__ = 'private_message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=False)
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)
    has_read = db.Column(db.Boolean, unique=False, default=False)
    create_time = db.Column(db.DateTime, unique=False)

    def __init__(self, content, create_user_id, to_user_id, has_read, create_time):
        self.content = content
        self.create_user_id = create_user_id
        self.to_user_id = to_user_id
        self.create_time = create_time
        self.has_read = has_read


def create_table():
    db.create_all()


def insert(content, create_user_id, to_user_id, create_time):
    insert = PrivateMessage(content=content, create_user_id=create_user_id, to_user_id=to_user_id, has_read=False,
                            create_time=create_time)
    db.session.add(insert)
    db.session.commit()
    return to_json(insert)


def select_all():
    data_all = PrivateMessage.query.all()
    return data_all


def select_by_id(id):
    data = PrivateMessage.query.get(id)
    return data


def select_user_message(create_user_id, to_user_id, page_no, num_per_page):  # think no_read over 10
    unread_count = PrivateMessage.query.filter_by(create_user_id=to_user_id, to_user_id=create_user_id,
                                                  has_read=False).order_by(asc(PrivateMessage.create_time)).count()
    if num_per_page < unread_count:
        num_per_page = unread_count
    data = PrivateMessage.query.filter(
        or_(and_(PrivateMessage.create_user_id == create_user_id, PrivateMessage.to_user_id == to_user_id),
            and_(PrivateMessage.create_user_id == to_user_id, PrivateMessage.to_user_id == create_user_id)),
        PrivateMessage.has_read==True
    ).order_by(desc(PrivateMessage.create_time)).paginate(page_no, num_per_page, False)
    return data.items


def select_new_message(create_user_id, to_user_id):  # think no_read over 10
    data = PrivateMessage.query.filter_by(create_user_id=create_user_id, to_user_id=to_user_id,
                                          has_read=False).order_by(asc(PrivateMessage.create_time)).all()
    return data


def delete(id):
    data = PrivateMessage.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return data


def update_has_read(id):
    row = PrivateMessage.query.get(id)
    row.has_read = int(True)
    print 'do update', row.id, row.has_read
    db.session.commit()


def select_recent_user(create_user_id, num_perpage):
#    # create_user==登录者  to_user == 最近聊天的人
#    sql = 'select max(tbl.id) as id from (' \
#          'SELECT pm1.id,pm1.content,pm1.to_user_id as create_user_id,pm1.create_user_id as to_user_id,pm1.has_read,create_time ' \
#          'FROM private_message pm1 ' \
#          'WHERE pm1.to_user_id =' \
#          + str(create_user_id) + \
#          ' union ' \
#          'SELECT * ' \
#          'FROM private_message pm2  ' \
#          'WHERE pm2.create_user_id =' \
#          + str(create_user_id) + \
#          ') tbl group by tbl.to_user_id'
#    rows = db.session.execute(sql).fetchall()
#
#    ids = []
#    for row in rows:
#        ids.append(str(int(row.id)))
#    data1 = PrivateMessage.query.filter_by(create_user_id=create_user_id).filter(PrivateMessage.id.in_(ids)).order_by(
#        desc(PrivateMessage.create_time))
#    data2 = db.session.query(PrivateMessage.id, PrivateMessage.content,
#                             PrivateMessage.to_user_id.label('create_user_id'),
#                             PrivateMessage.create_user_id.label('to_user_id'), PrivateMessage.has_read,
#                             PrivateMessage.create_time).filter_by(to_user_id=create_user_id).filter(
#        PrivateMessage.id.in_(ids)).order_by(desc(PrivateMessage.create_time)).order_by(
#        desc(PrivateMessage.create_time))
#    data = data1.union(data2).group_by(PrivateMessage.create_user_id, PrivateMessage.to_user_id).order_by(
#        desc(PrivateMessage.create_time)).limit(num_perpage)
#    to_user_list = []
#    for private_message in data:
#        to_user_list.append(private_message.touser)
#    return to_user_list

    user_recently={}
    sql1='select create_user_id,max(create_time) as max_create_time from private_message \
        where to_user_id=' + str(create_user_id) +' group by create_user_id '\
        +' order by max_create_time desc limit '+str(num_perpage)
    rows = db.session.execute(sql1).fetchall()
    for row in rows:
      user_recently[str(int(row.create_user_id))]=str(row.max_create_time)

    sql2='select to_user_id,max(create_time) as max_create_time from private_message \
        where create_user_id=' + str(create_user_id) +' group by to_user_id '\
        +' order by max_create_time desc limit '+str(num_perpage)
    rows2 = db.session.execute(sql2).fetchall()
    for row in rows2:
      user_recently[str(int(row.to_user_id))]=str(row.max_create_time)

    sorted_user_recently=sorted(user_recently.iteritems(),key=lambda asd:asd[1],reverse=True)

    user_list=[]
    count=0
    for item in sorted_user_recently:
      print item 
      if item[0] != str(create_user_id):
        if count < num_perpage:
          user_list.append(db_model_user.select_by_id(int(item[0])))
          count=count+1
    
    return user_list

# 查询未读私信条数
def select_all_unread(to_user_id):
    count = PrivateMessage.query.filter_by(to_user_id=to_user_id, has_read=False).count()
    return count


def select_unread_by_each_user(create_user_id, to_user_id):
    count = PrivateMessage.query.filter_by(create_user_id=create_user_id, to_user_id=to_user_id, has_read=False).count()
    print 'unread count', count, 'to_user_id', to_user_id, 'create_user_id', create_user_id
    return count


def to_json(object):
    if isinstance(object, PrivateMessage):
        return {
            'id': object.id,
            'content': object.content,
            'create_user_id': object.create_user_id,
            'to_user_id': object.to_user_id,
            'create_time': object.create_time,
            'has_read': object.has_read,
            'user': db_model_user.to_json(object.user),
            'touser': db_model_user.to_json(object.touser)

        }
