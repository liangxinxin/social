#coding=utf-8
import time
import math
import json
from flask import session

from db_interface import db_model_message
from db_interface import db_model_user
from db_interface import db_model_post
from db_interface import db_model_reply
from db_interface import db_model_user_relation
import time_format

default_page_no = 1
default_num_perpage = 10
default_community_id = 0
default_post_id = 0
default_relation = 0
has_relation = 1
cancel_relation = 2
default_relation_id = 0
max_num_perpage =100


def service(request):
    print "enter do user create service"
    if request.method == 'POST':
        type = request.form.get("type")
        if type == "publish":
            return create_user(request)
        else:
            print "error request:", request
    elif request.method == 'GET':

        user_id = request.args.get("user_id", 0)
        if user_id != 0:
            return query_user_info(request)


def create_user(request):
    print "now create new user request"
    # insert to db
    name = request.form.get("name")
    password = request.form.get("password")
    mobile = request.form.get("mobile", 0)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    print 'name:', name, 'mobile:', mobile
    print "now insert to db"
    db_model_user.insert(name=name, password=password, mobile=mobile)

    # return select value
    user = db_model_user.select_by_name_and_password_and_mobile(name=name, password=password, mobile=mobile)
    if user != None:
        session['userinfo'] = {'name': user.name, 'id': user.id}
    return


#  rt=jsonify(result="succ",name=name,mobile=mobile) 

def query_user_info(request):
    print "now query user info from id"
    user_id = request.args.get("user_id")
    user_info = db_model_user.select_by_id(user_id)
    return user_info

def get_user_post(request):
    user_id = request.args.get("user_id")
    page_no = int(request.args.get("no", default_page_no))
    num_perpage = int(request.args.get("size", default_num_perpage))
    paginate = db_model_post.select_all_by_user(page_no,num_perpage,user_id)
    post_list = []
    for post in paginate.items:
        post.create_time = time_format.timestampFormat(post.create_time)
        post_list.append(db_model_post.to_json(post))
    return post_list,page_no,num_perpage,paginate.total

def add_relation(request):
    print "now create user relation"
    # insert db
    user_id = session.get('userinfo')['id']
    login_user =db_model_user.select_by_id(user_id)
    relation_user_id = request.form.get("relation_user_id")
    relation_user = db_model_user.select_by_id(relation_user_id)

    data = db_model_user_relation.select_by_user_id(user_id, relation_user_id)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    if data != None:
        db_model_user_relation.update(user_id, relation_user_id, has_relation, update_time)
    else:
        create_time = update_time
        print 'user_id', user_id, 'relation_user_id', relation_user_id
        db_model_user_relation.insert(user_id, relation_user_id, has_relation, create_time, update_time)
        #write message
        db_model_message.insert_follow(user_id,relation_user_id)

    login_user.attention_num = login_user.attention_num + 1
    print "now update user attention_num", login_user.attention_num
    db_model_user.update_user(login_user)
    relation_user.by_attention_num = relation_user.by_attention_num + 1
    print "now update user by_attention_num", relation_user.by_attention_num
    db_model_user.update_user(relation_user)

def update_relation(request):
    print "now update user relation"
    # update  is_relation = 1
    user_id = session.get('userinfo')['id']
    login_user = db_model_user.select_by_id(user_id)
    relation_user_id = request.form.get("relation_user_id", 0)
    relation_user=db_model_user.select_by_id(relation_user_id)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    db_model_user_relation.update(user_id, relation_user_id, cancel_relation, update_time)

    login_user.attention_num = login_user.attention_num - 1
    db_model_user.update_user(login_user)
    print "now update user attention_num", login_user.attention_num

    relation_user.by_attention_num = relation_user.by_attention_num -1
    print "now update user by_attention_num",relation_user.by_attention_num
    db_model_user.update_user(relation_user)


def select_relation_user_id(request):
    print "now select user relation"
    # select db
    user_id = session.get('userinfo')['id']
    relation_user_id = request.form.get("relation_user_id", 0)
    user_relation = db_model_user_relation.select_by_user_id(user_id, relation_user_id)
    if user_relation != None:
        return user_relation.is_relation
    else:
        return default_relation


def get_unread_message_from_session():
    user_id = 0
    if session.get('userinfo') != None:
        user_id = (int)(session.get('userinfo')['id'])
    user_info = db_model_user.select_by_id(user_id)
    messages = None
    if user_info != None:
        messages=user_info.to_user_messages.filter_by(has_read=False).all()
        print "message-------------",len(messages)
    return messages

def check_login():
    login_flag = False
    if session.get('userinfo')!=None:
        login_flag = True
    return login_flag


def good_friends(request):
    user_id = request.args.get("user_id")
    login_user_id=0
    print 'into good friends user_id:',user_id
    if session.get('userinfo') != None:
        login_user_id = (int)(session.get('userinfo')['id'])
    page_no = int(request.args.get("no",default_page_no))
    num_perpage = int(request.args.get("size", default_num_perpage))
    each_attention = True
    paginate = db_model_user_relation.seletct_good_friends(user_id,each_attention,page_no, num_perpage)
    print 'total friends',paginate.total
    json_user=[]


    if login_user_id==0:
        for user_relation in paginate.items:
            user_relation= db_model_user_relation.to_json(user_relation)
            user_relation['is_relation']=False
            json_user.append(user_relation)
    else:
        for user_relation in paginate.items:
            #当前登录的人是否关注个人主页好友
            login_user_relation =db_model_user_relation.select_by_relation(login_user_id,user_relation.user_id,has_relation)
            user_relation= db_model_user_relation.to_json(user_relation)
            if login_user_relation==None:
                user_relation['is_relation'] = False
            else:
                user_relation['is_relation'] =True


            json_user.append(user_relation)

    return json_user,page_no,num_perpage,paginate.total

