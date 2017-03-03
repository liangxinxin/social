import time

from flask import session

from db_interface import db_model_message
from db_interface import db_model_user
from db_interface import db_model_user_relation

default_page_no = 1
default_num_perpage = 20
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
    mobile = '0' 
    if session['userinfo'] !=None:
        mobile=session['userinfo']['mobile']
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    print 'name:', name, 'mobile:', mobile
    print "now insert to db"
    db_model_user.insert(name=name, password=password, mobile=mobile)

    # return select value
    user = db_model_user.select_by_mobile(mobile=mobile)
    if user != None:
        print 'now update session info'
        if session['userinfo'] == None:
            print 'now create session info'
            session['userinfo'] = {'name': user.name, 'id': user.id}
        else:
            print 'now add session info'
            session['userinfo'] = {'mobile':mobile,'name': user.name, 'id': user.id}
           # session['userinfo']['name'] = user.name
           # session['userinfo']['id'] = user.id
    print 'after create user,session is:',session
    return user


#  rt=jsonify(result="succ",name=name,mobile=mobile) 

def query_user_info(request):
    user_id = request.args.get("user_id")
    user_info = db_model_user.select_by_id(user_id)
    return user_info



def add_relation(request):
    print "now create user relation"
    # insert db
    user_id = session.get('userinfo')['id']
    relation_user_id = request.form.get("relation_user_id")
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


def update_relation(request):
    print "now update user relation"
    # update  is_relation = 1
    user_id = session.get('userinfo')['id']
    relation_user_id = request.form.get("relation_user_id", 0)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    db_model_user_relation.update(user_id, relation_user_id, cancel_relation, update_time)


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
        print ' get unread message ,session is :',session
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


