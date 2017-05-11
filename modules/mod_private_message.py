# coding=utf-8
import json
import time

from flask import session

from db_interface import db_model_action
from db_interface import db_model_action_type
from db_interface import db_model_private_message
from db_interface import db_model_user

default_page_no = 1
default_num_perpage = 10


def service(request):
    if request.method == 'POST':
        type = request.form.get('type')
        if type == 'send':
            return save_private_message(request)
    else:
        type = request.args.get('type')
        if type == 'recent_user':
            return select_recent_user(request)
        elif type == 'new_message':
            return select_new_message(request)
        elif type == 'history_message':
            return select_mess_by_user(request)


def select_recent_user(request):
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        to_user_id = request.args.get('to_user_id', 0)  # after click private_mess btn
        user_list = []  # recent chat user
        unread_count_list = []  # unread message count
        to_user = None
        if to_user_id > 0:  # have click private_mess
            to_user = db_model_user.select_by_id(to_user_id)
        num_perpage = request.args.get('num_perpage', default_num_perpage)
        to_user_list = db_model_private_message.select_recent_user(user_id, num_perpage)  # 返回最近聊天的人
        for user in to_user_list:
            # 查询未读的消息条数
            if user != to_user:
                count = db_model_private_message.select_unread_by_each_user(user.id, user_id)
                unread_count_list.append(int(count))
                user_list.append(user)
        user_num = len(user_list)
        return to_user, user_list, unread_count_list, user_num


def select_mess_by_user(request):
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        to_user_id = int(request.args.get('to_user_id', 0))  # after click user
        page_no = int(request.args.get('page_no', default_page_no))
        num_perpage = int(request.args.get('num_perpage', default_num_perpage))
        data = db_model_private_message.select_user_message(user_id, to_user_id, page_no, num_perpage)
        mess_list = []
        for message in data:
            mess_list.append(db_model_private_message.to_json(message))
        mess_list.reverse()
        return mess_list


def select_new_message(request):
    print 'into new mess'
    if session.get('userinfo'):
        to_user_id = int(session.get('userinfo')['id'])
        create_user_id = int(request.args.get('create_user_id'))
        new_messaage = db_model_private_message.select_new_message(create_user_id, to_user_id)
        mess_list = []
        for message in new_messaage:
            mess_list.append(db_model_private_message.to_json(message))
            db_model_private_message.update_has_read(message.id)
    return mess_list


def save_private_message(request):
    result = {}
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        to_user_id = request.form.get('to_user_id')
        content = request.form.get('content')
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        message = db_model_private_message.insert(content, user_id, to_user_id, create_time)
        result['code'] = 0
        result['message'] = 'success'
        result['data'] = message
        print "record action of create private message"
        action_content = {'from_user_id': user_id, 'to_user_id': to_user_id, 'message_id': message['id']}
        db_model_action.insert(user_id=user_id, action_type_id=db_model_action_type.get_type_id('create_private'),
                               action_detail_info=json.dumps(action_content, ensure_ascii=False),
                               create_time=create_time)
    else:
        result['code'] = 1
        result['message'] = 'fail'
        result['data'] = ''
    return result
