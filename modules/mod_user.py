# coding=utf-8
import time
import time_format
import json
from db_interface import db_model_message
from db_interface import db_model_post
from db_interface import db_model_user
from db_interface import db_model_user_relation
from db_interface import db_model_action
from db_interface import db_model_action_type
from db_interface import db_model_community
from flask import session
from Logger import *

default_page_no = 1
default_num_perpage = 10
default_community_id = 0
default_post_id = 0
default_relation = 0
has_relation = 1
cancel_relation = 2
default_relation_id = 0
max_num_perpage = 100


def service(request):
    Logger.infoLogger.info('enter user  service')
    if request.method == 'POST':
        type = request.form.get("type")
        if type == "create":
            return create_user(request)
        elif type == "modify":
            return modify_user_from_mobile(request)
        elif type == "check_user_name":
            return check_user_name(request)
        elif type == "modify_password":
            return modify_password(request)
        else:
            Logger.infoLogger.error('error request:%s',request)
    elif request.method == 'GET':
            user_id = request.args.get("user_id")
            if user_id > 0:
                return query_user_info(user_id) ## 查询个人主页，
            else:
                return query_login_user_info()


def create_user(request):
    Logger.infoLogger.info('now create new user ')
    # insert to db
    mobile = request.form.get("mobile")
    password = request.form.get("password")
    Logger.infoLogger.info('password:%s,mobile:%s',password, mobile)
    Logger.infoLogger.info('now insert to db')
    db_model_user.insert(name=mobile, password=password, mobile=mobile)

    # return select value
    user = db_model_user.select_by_mobile(mobile=mobile)
    if user:
        Logger.infoLogger.info('now update session info')
        if session['userinfo'] is None:
            Logger.infoLogger.info('now create session info')
            session['userinfo'] = {'name': user.name, 'id': user.id}
        else:
            Logger.infoLogger.info('now add session info')
            session['userinfo'] = {'mobile': mobile, 'name': user.name, 'id': user.id}
            Logger.infoLogger.info('record action user regist:')
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        db_model_action.insert(user_id=user.id, \
                               action_type_id=db_model_action_type.get_type_id('regist'), action_detail_info='', \
                               create_time=create_time)
        Logger.infoLogger.info('after create user,session is:%s', session)
        result = {'code': '0', 'succ': '0','message': 'create user succ!'}
    else:
        result = {'code': '1', 'succ': '1', 'message': 'create user fail!'}
        Logger.infoLogger.error('result:%s', result)
    Logger.infoLogger.info('result:%s', result)
    return result, user


def modify_user_from_mobile(request):
    Logger.infoLogger.info('now modify  user info  from mobile')
    # insert to db
    result = {'succ': '1'}
    name = request.form.get("name")
    label = request.form.get("label")
    mobile = request.form.get("mobile")
    if name is None or label is None or mobile is None:
        result['code'] = '1'
        result['message'] = 'name or lable or mobile is null'
        Logger.infoLogger.error('result:%s', result)
    else:
        user = db_model_user.select_by_mobile(mobile)
        if user:
            user.name = name
            user.label = label
            db_model_user.update_user(user)
            session['userinfo'] = {'mobile': mobile, 'name': user.name, 'id': user.id}
            result['succ'] = '0'
            result['code'] = '0'
            result['message'] = 'fill user info succ!'
            Logger.infoLogger.info('result:%s', result)
    return result


def modify_password(request):
    Logger.infoLogger.info('now modify  user password  from mobile')
    # insert to db
    result = {'succ': '1'}
    mobile = request.form.get("mobile")
    password = request.form.get("password")
    if password is None or mobile is None:
        result['code'] = '1'
        result['message'] = 'password or mobile is null'
        Logger.infoLogger.error('result:%s',result)
    else:
        user = db_model_user.select_by_mobile(mobile)
        if user:
            user.password = password
            db_model_user.update_user(user)
            session['userinfo'] = {'mobile': mobile, 'name': user.name, 'id': user.id}
            result['succ'] = '0'
            result['code'] = '0'
            result['message'] = 'modify password succ!'
            Logger.infoLogger.info('result:%s', result)
    return result


def check_user_name(request):
    name = request.form.get("name")
    Logger.infoLogger.info('check user name:%s', name)
    result = {'succ': 1}
    if name is None or name == '':
        result['succ'] = '0'
        result['code'] = '0'
        result['message'] = 'check user name pass!'
    else:
        user = db_model_user.select_full_match_by_name(name)
        Logger.infoLogger.info('query name result:%s,%s', (name, user))
        if user:
            result['succ'] = '1'
            result['code'] = '1'
            result['message'] = 'user have exist!'
        else:
            result['succ'] = '0'
            result['code'] = '0'
            result['message'] = 'check user name pass!'
    Logger.infoLogger.info('result:%s', result)
    return result


def query_user_info(user_id):
    Logger.infoLogger.info('now query  user info,id：%s',user_id)
    user_info = db_model_user.select_by_id(user_id)
    return user_info


def query_login_user_info():
    user_info = None
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        user_info = db_model_user.select_by_id(user_id)
        return user_info
    else:
        return user_info

def get_user_post(request):
    user_id = request.args.get("user_id")
    view_user_info = db_model_user.select_by_id(user_id)
    page_no = int(request.args.get("no", default_page_no))
    num_perpage = int(request.args.get("size", default_num_perpage))
    paginate = db_model_post.select_all_by_user(page_no, num_perpage, user_id)
    post_list = []
    for post in paginate.items:
        post.create_time = time_format.timestampFormat(post.create_time)
        post_list.append(post)
    return post_list, page_no, num_perpage, paginate.total, view_user_info


def add_relation(request):
    Logger.infoLogger.info('now create user relation')
    # insert db
    user_id = session.get('userinfo')['id']
    login_user = db_model_user.select_by_id(user_id)
    relation_user_id = request.form.get("relation_user_id")
    relation_user = db_model_user.select_by_id(relation_user_id)

    Logger.infoLogger.info('login_user_id:%s,relation_user_id:%s',user_id,relation_user_id)
    data = db_model_user_relation.select_by_user_id(user_id, relation_user_id)
    relation_data = db_model_user_relation.select_by_user_id(relation_user_id, user_id)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    # update by lxx,2017-04-19 start
    if data is None:
        each_attention = False
        if relation_data and relation_data.is_relation:
            each_attention = True
        create_time = update_time
        Logger.infoLogger.info('user_id:%s,relation_user_id:%s', user_id,relation_user_id)
        db_model_user_relation.insert(user_id, relation_user_id, has_relation, create_time, update_time, each_attention)
        if each_attention:
            relation_data.each_attention = each_attention
            relation_data.create_time = create_time
            db_model_user_relation.update(relation_data)
        # write message
        db_model_message.insert_follow(user_id, relation_user_id)
    elif data and relation_data:
        data.is_relation = True
        if data.is_relation and relation_data.is_relation:
            data.each_attention = True
            data.update_time = update_time
            relation_data.each_attention = True
            relation_data.update_time = update_time
            db_model_user_relation.update(data)
            db_model_user_relation.update(relation_data)
    else:
        data.is_relation = True
        data.update_time = update_time
        db_model_user_relation.update(data)
    # end
        Logger.infoLogger.info('record action of follow user')
    action_content = {'user_id': user_id, 'to_user_id': relation_user_id}
    db_model_action.insert(user_id=user_id, action_type_id=db_model_action_type.get_type_id('follow'),
                           action_detail_info=json.dumps(action_content, ensure_ascii=False),
                           create_time=update_time)

    login_user.attention_num += 1
    Logger.infoLogger.info('now update user attention_num:%s', login_user.attention_num)
    db_model_user.update_user(login_user)
    relation_user.by_attention_num += 1
    Logger.infoLogger.info('now update user by_attention_num:%s', relation_user.by_attention_num)
    db_model_user.update_user(relation_user)


def update_relation(request):  # cancel
    Logger.infoLogger.info('now update user relation')
    # update  is_relation = 1
    user_id = session.get('userinfo')['id']
    login_user = db_model_user.select_by_id(user_id)
    relation_user_id = request.form.get("relation_user_id", 0)
    user = db_model_user.select_by_id(relation_user_id)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    update_time = time.strftime(ISOTIMEFORMAT, time.localtime())

    # cancel attention ,update by lxx,2017-04-19 start
    user_relation = db_model_user_relation.select_by_user_id(user_id, relation_user_id)
    if user_relation.is_relation:
        user_relation.is_relation = False
        user_relation.update_time = update_time
        if user_relation.each_attention:
            user_relation.each_attention = False
            relation_user = db_model_user_relation.select_by_user_id(relation_user_id, user_id)
            relation_user.each_attention = False
            relation_user.update_time = update_time
            db_model_user_relation.update(relation_user)
        db_model_user_relation.update(user_relation)
    # end
    Logger.infoLogger.info('record action of cancel follow user')
    action_content = {'user_id': user_id, 'to_user_id': relation_user_id}
    db_model_action.insert(user_id=user_id, action_type_id=db_model_action_type.get_type_id('cancel_follow'),
                           action_detail_info=json.dumps(action_content, ensure_ascii=False), create_time=update_time)

    login_user.attention_num -= 1
    db_model_user.update_user(login_user)
    Logger.infoLogger.info('now update user attention_num:%s', login_user.attention_num)

    user.by_attention_num -= 1
    Logger.infoLogger.info('now update user by_attention_num:%s', user.by_attention_num)
    db_model_user.update_user(user)


def select_relation_user_id(request):
    Logger.infoLogger.info('now select user relation')
    # select db
    user_id = session.get('userinfo')['id']
    relation_user_id = request.form.get("relation_user_id", 0)
    Logger.infoLogger.info('user_id:%s,relation_user_id:%s', int(user_id), relation_user_id)
    user_relation = db_model_user_relation.select_by_user_id(user_id, relation_user_id)
    if user_relation:
        return user_relation.is_relation
    else:
        return default_relation


def get_unread_message_from_session():
    messages_unread_len = 0
    if session.get('userinfo'):
        Logger.infoLogger.info('get unread message ,session is :%s', session)
        user_id = int(session.get('userinfo')['id'])
        user_info = db_model_user.select_by_id(user_id)
        if user_info:
            messages = user_info.to_user_messages.filter_by(has_read=False).all()
            messages.extend(user_info.private_mess_to_user.filter_by(has_read=False).all())
            messages_unread_len = len(messages)
        Logger.infoLogger.info('unread message length: %s',messages_unread_len)

    return messages_unread_len


def check_login():
    login_flag = False
    if session.get('userinfo'):
        login_flag = True
    return login_flag


def good_friends(request):
    user_id = request.args.get("user_id")
    view_user_info = db_model_user.select_by_id(user_id)
    login_user_id = 0
    Logger.infoLogger.info('into good friends user_id:%s', user_id)
    if session.get('userinfo'):
        login_user_id = int(session.get('userinfo')['id'])
    page_no = int(request.args.get("no", default_page_no))
    num_perpage = int(request.args.get("size", default_num_perpage))
    each_attention = True
    paginate = db_model_user_relation.select_good_friends(user_id, each_attention, page_no, num_perpage)
    Logger.infoLogger.info('total friends:%s', paginate.total)
    json_user = []

    if login_user_id == 0:
        for user_relation in paginate.items:
            user_relation.is_relation = False
            json_user.append(user_relation)
    else:
        for user_relation in paginate.items:
            # 当前登录的人是否关注个人主页好友
            login_user_relation = db_model_user_relation.select_by_relation(login_user_id, user_relation.user_id,
                                                                            has_relation)
            if login_user_relation == None:
                user_relation.is_relation = False
            else:
                user_relation.is_relation = True

            json_user.append(user_relation)

    return json_user, page_no, num_perpage, paginate.total, view_user_info


def community_create(request):
    user_id = request.args.get("user_id")
    view_user_info = db_model_user.select_by_id(user_id)
    Logger.infoLogger.info('into community owned user_id:%s', user_id)
    page_no = int(request.args.get("no", default_page_no))
    num_perpage = int(request.args.get("size", default_num_perpage))
    paginate = db_model_community.select_by_owner_id_paging(user_id, page_no, num_perpage)
    Logger.infoLogger.info('total community:%s', paginate.total)
    community_list = []
    for item in paginate.items:
        community_list.append(item)
    return community_list, page_no, num_perpage, paginate.total, view_user_info


def update_user(request):
    result = {}
    if session.get('userinfo')['id']:
        try:
            userid = int(session.get('userinfo')['id'])
            user = db_model_user.select_by_id(userid)
            username = request.form.get('user_name')
            user.name = username
            label = request.form.get('user_label')
            user.label = label
            Logger.infoLogger.info('after modify:%s,%s',user.name, user.label)
            db_model_user.update_user(user)
            session['userinfo'] = {'name': user.name, 'id': user.id}
            result['succ'] = '0'
            result['code'] = '0'
            result['message'] = 'update user info succ!'
            Logger.infoLogger.info('result:%s',result)
        except Exception, e:
            result['code'] = 1
            result['message'] = 'exception'
            Logger.infoLogger.error('Exception:%s', e)

    else:
        result['code'] = 1
        request['message'] = 'user not login'
        Logger.infoLogger.info('result:%s', result)
    return result
