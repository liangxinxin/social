# coding=utf-8

from sqlalchemy import desc,func
import  db_model_user
from db_connect import db


class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1500), unique=False)
    content = db.Column(db.Text, unique=False)
    floor_num = db.Column(db.Integer, unique=False)
    community_id = db.Column(db.Integer,db.ForeignKey('community.id'))
    create_time = db.Column(db.DateTime, unique=False)
    last_update_time = db.Column(db.DateTime, unique=False)
    create_user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    status =db.Column(db.Boolean,unique=False,default=0)
    messages = db.relationship('Message',backref='post',lazy='dynamic')
    replys = db.relationship('Reply',backref='post',lazy='dynamic')


    def __init__(self, title, content, create_user_id, community_id, floor_num, create_time, last_update_time,status):
        self.title = title
        self.content = content
        self.create_user_id = create_user_id
        self.community_id = community_id
        self.floor_num = floor_num
        self.create_time = create_time
        self.last_update_time = last_update_time
        self.status=status


def create_table():
    db.create_all()


def insert(title, content, create_user_id, community_id, floor_num, create_time, last_update_time,status):
    insert = Post(title=title, content=content, create_user_id=create_user_id, community_id=community_id,
                  floor_num=floor_num, create_time=create_time, last_update_time=last_update_time,status=status)
    db.session.add(insert)
    db.session.commit()
    return insert


def select_by_ids(ids,page_no, num_per_page):
    #按ids顺序返回 find_in_set
    paginate = Post.query.filter(Post.status == 0,func.find_in_set(Post.id,ids)).paginate(page_no, num_per_page,False)
    return paginate
def select_all():
    data_all = Post.query.filter(Post.status==0).all()
    return data_all

def select_by_id(id):
    data = Post.query.filter(Post.status==0,Post.id==id).first()
    return data


def update(id, title, content, create_user_id, community_id, floor_num, create_time, last_update_time,status):
    row = Post.query.get(id)
    row.title = title
    row.content = content
    row.create_user_id = create_user_id
    row.community_id = community_id
    row.floor_num = floor_num
    row.create_time = create_time
    row.last_update_time = last_update_time
    row.status = status
    db.session.commit()



def update(post):
    row = Post.query.get(post.id)
    row.title = post.title
    row.content = post.content
    row.create_user_id = post.create_user_id
    row.community_id = post.community_id
    row.floor_num = post.floor_num
    row.create_time = post.create_time
    row.last_update_time = post.last_update_time
    row.status = post.status
    db.session.commit()


def delete(id):
    data = Post.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return data


def select_by_title(title):
    filter_string = "%" + title + "%"
    data = Post.query.filter(Post.title.like(filter_string),Post.status==0)
    return data


def select_by_title_paging(title, page_no, num_per_page):
    filter_string = "%" + title + "%"
    paginate = Post.query.filter(Post.title.like(filter_string),Post.status==0).order_by(desc(Post.id)).paginate(page_no, num_per_page,
                                                                                                  False)
    return paginate


# return paginate
def select_all_paging(page_no, num_per_page, community_id):
    print 'no:', page_no, 'num:', num_per_page, 'commu id:', community_id
    if page_no < 1:
        page_no = 1
    paginate = Post.query.filter(Post.community_id == community_id,Post.status==0).order_by(desc(Post.create_time)).paginate(page_no,
                                                                                                              num_per_page,
                                                                                                              False)
    print paginate
    return paginate


# return paginate
def select_post_by_floor_num(page_no, num_per_page):
    print 'no:', page_no, 'num:', num_per_page
    if page_no < 1:
        page_no = 1
    paginate = Post.query.filter(Post.status==0).order_by(desc(Post.floor_num)).paginate(page_no, num_per_page, False)
    print paginate
    return paginate

# return paginate
def select_all_by_user(page_no, num_per_page, user_id):
    print 'no:', page_no, 'num:', num_per_page, 'user_id:', user_id
    if page_no < 1:
        page_no = 1
    paginate = Post.query.filter(Post.create_user_id == user_id,Post.status==0).order_by(desc(Post.create_time)).paginate(page_no,num_per_page, False)
    return paginate

def to_json(object):
    if isinstance(object, Post):
        return {
            'id':object.id,
            'title': object.title,
            'content': object.content,
            'create_user_id':object.create_user_id,
            'user':db_model_user.to_json(object.user),
            'community_id':object.community_id,
            'floor_num':object.floor_num,
            'create_time':object.create_time,
            'last_update_time':object.last_update_time,
            'status':object.status
        }

def select_by_title_user_id_community_id(title,user_id,community_id):
    data = Post.query.filter(Post.title==title,Post.create_user_id==user_id,Post.community_id==community_id)
    return data
