# coding=utf-8
import json
import time
import mod_base64
import time_format
from flask import session
from db_interface import db_model_action
from db_interface import db_model_action_type
from db_interface import db_model_message
from db_interface import db_model_post
from db_interface import db_model_reply
from db_interface import db_model_reply_like_stat
from db_interface import db_model_user
from db_interface import db_model_comment

default_page_no = 1
default_num_perpage = 10


def service(request):
    if request.method == 'POST':
        type = request.form.get('type')
        if type == 'publish':
            return publish_reply(request)
        elif type == 'delete':
            return delete_reply(request)
        elif type == 'update':
            return update_reply(request)
        else:
            print 'error request:', request
    elif request.method == 'GET':
        type = request.args.get('type')
        if type == 'query':
            return get_reply_by_post(request)
        print 'hehe,the request is:', request


def reply_like_changed(request):
    if session.get('userinfo'):
        print "'user's info-------\n'", session.get('userinfo')
        user_id = session.get('userinfo')['id']
        reply_id = request.form.get('reply_id')
        mod_type = request.form.get('mod_type')
        reply = db_model_reply.select_by_id(reply_id)
        result = {'code': 0}
        if reply:
            ISOTIMEFORMAT = '%Y-%m-%d %X'
            if mod_type == 'add':
                create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
                db_model_reply_like_stat.insert(reply_id, user_id, create_time)
                db_model_message.insert_zan_reply(user_id, reply_id)
                reply.like_num += 1
                db_model_reply.update_like_num(reply_id, reply.like_num, create_time)
                print 'record action of like reply'
                action_content = {'reply_id': reply.id}
                db_model_action.insert(user_id=user_id,
                                       action_type_id=db_model_action_type.get_type_id('praise_reply'),
                                       action_detail_info=json.dumps(action_content, ensure_ascii=False),
                                       create_time=create_time)
            else:
                last_update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
                db_model_reply_like_stat.remove(reply_id, user_id)
                print ' remove reply_like_stat id', reply_id, 'user_id', user_id
                reply.like_num -= 1
                db_model_reply.update_like_num(reply_id, reply.like_num, last_update_time)

            result['code'] = 0
            result['message'] = 'success'
            result['like_num'] = reply.like_num
        else:
            result['code'] = 1
            result['message'] = 'reply is null'

        return result


def get_reply_by_post(request):
    login_user_id = 0
    reply_list = []
    like_user_dict = {}
    # this is load comment
    comment_page_no = 1
    page_no = int(request.args.get('page_no', default_page_no))
    num_perpage = int(request.args.get('num_perpage', default_num_perpage))  # 回帖加载条数
    comment_num_perpage = int(request.args.get('comment_num_perpage', default_num_perpage))  # 回复加载条数

    if session.get('userinfo'):
        login_user_id = session.get('userinfo')['id']
    post_id = request.args.get('post_id')
    best_reply = db_model_reply.select_best_by_post_id(post_id)

    if best_reply:
        like_user_dict[best_reply.id] = select_like_user(best_reply.id)
        paginate = db_model_reply.select_except_best_id(page_no, num_perpage, post_id, best_reply.id)
        best_reply.last_update_time = time_format.timestampFormat(best_reply.last_update_time)
        best_reply_comment_paginate = best_reply.comments.filter(db_model_comment.Comment.status == 0).paginate(
            page_no, comment_num_perpage, False)
        best_comment = []
        for comment in best_reply_comment_paginate.items:
            comment.create_time = time_format.timestampFormat(comment.create_time)
            best_comment.append(db_model_comment.to_json(comment))
        is_like_best = db_model_reply_like_stat.is_reply_liked_by_user(best_reply.id, login_user_id)
        best_reply = db_model_reply.to_json(best_reply)
        best_reply['like_user'] = select_like_user(best_reply['id'])
        best_reply['comments'] = best_comment
        best_reply['is_like'] = is_like_best
    else:
        paginate = db_model_reply.select_paging_by_post_id(page_no, num_perpage, post_id)

    for reply in paginate.items:
        is_like = db_model_reply_like_stat.is_reply_liked_by_user(reply.id, login_user_id)
        reply.last_update_time = time_format.timestampFormat(reply.last_update_time)
        comment_list = []
        comment_paginate = reply.comments.filter(db_model_comment.Comment.status == 0).paginate(comment_page_no,
                                                                                                comment_num_perpage,
                                                                                                False)
        for comment in comment_paginate.items:
            comment.create_time = time_format.timestampFormat(comment.create_time)
            comment_list.append(db_model_comment.to_json(comment))
        reply = db_model_reply.to_json(reply)
        reply['like_user'] = select_like_user(reply['id'])
        reply['comments'] = comment_list
        reply['islike'] = is_like
        reply_list.append(reply)
    total = paginate.total
    total_page = paginate.pages

    return reply_list, best_reply, like_user_dict, page_no, num_perpage, total_page, total


def publish_reply(request):
    if session.get('userinfo'):
        create_user_id = int(session.get('userinfo')['id'])
        content = request.form.get('content')
        post_id = int(request.form.get('post_id'))
        has_best = request.form.get('has_best')
        community_id = int(request.form.get('community_id', 0))
        num_perpage = int(request.form.get('num_perpage', default_num_perpage))
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        post_data = db_model_post.select_by_id(post_id)
        floor = post_data.floor_num + 1
        post_data.floor_num += 1
        db_model_post.update(post_data)
        floor_num = 0
        like_num = 0
        status = 0
        last_update_time = create_time
        path_type = 'reply'
        content = mod_base64.base64_hander(content, path_type)
        print 'create reply--- content:', content, 'user_id:', create_user_id, 'post_id:', post_id,'community_id',\
            community_id
        # insert to db
        db_model_reply.insert(content, create_user_id, post_id, floor, floor_num, like_num, create_time, status,
                              last_update_time)
        reply = db_model_reply.select_by_create_user_and_post_and_floor(create_user_id, post_id, floor)
        if reply and (create_user_id != post_data.create_user_id):
            db_model_message.insert_reply_post(create_user_id, post_id, reply.id)
            print 'record action of create reply'
            action_content = {'reply_id': reply.id}
            db_model_action.insert(user_id=create_user_id,
                                   action_type_id=db_model_action_type.get_type_id('create_reply'),
                                   action_detail_info=json.dumps(action_content, ensure_ascii=False),
                                   create_time=create_time)
        print 'now insert to db'
        reply.create_time = time_format.timestampFormat(reply.create_time)
        reply = db_model_reply.to_json(reply)
        replycount = post_data.floor_num
        if replycount <= num_perpage:
            total_page = 1
            return reply, replycount, total_page
        if has_best == 'true':
            replycount -= 1
        if replycount % num_perpage == 0:
            total_page = replycount / num_perpage
        else:
            total_page = replycount / num_perpage + 1

        return reply, replycount, total_page


def update_reply(request):
    result = {}
    content = request.form.get('content')
    reply_id = request.form.get('reply_id')
    reply = db_model_reply.select_by_id(reply_id)
    if reply:
        print 'reply is none', reply_id
        result['code'] = 1
    reply.content = content
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    reply.last_update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    result['code'] = 0
    try:
        db_model_reply.update(reply)
    except Exception, e:
        result['code'] = 1
        print e

    return result


def delete_reply(request):
    result = {'code': 0, 'replycount': 0}
    reply_id = long(request.form.get('reply_id'))
    reply = db_model_reply.select_by_id(reply_id)
    if reply is None:
        print 'reply is none', reply_id
        result['code'] = 1
        return result
    reply.status = 1
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    last_update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    reply.last_update_time = last_update_time
    try:
        db_model_reply.update(reply)
        post = db_model_post.select_by_id(reply.post_id)
        if post.floor_num > 0:
            post.floor_num -= 1
        db_model_post.update(post)
        result['replycount'] = post.floor_num
    except Exception, e:
        result['code'] = 1
        print e
    return result


def select_like_user(reply_id):
    num_perpage = 10
    paginate = db_model_reply_like_stat.like_user(reply_id, default_page_no, num_perpage)
    user_list = []
    for item in paginate.items:
        user = db_model_user.select_by_id(item.user_id)
        user_list.append(db_model_user.to_json(user))
    return user_list
