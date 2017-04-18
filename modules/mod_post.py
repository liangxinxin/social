# coding=utf-8
import json
import time

import jieba
from flask import session

from db_interface import db_model_action
from db_interface import db_model_action_type
from db_interface import db_model_community
from db_interface import db_model_inverted_index
from db_interface import db_model_post
from db_interface import db_model_reply
from db_interface import db_model_reply_like_stat
from db_interface import db_model_user
from db_interface import db_model_user_community
from modules import mod_base64
from modules import mod_lcs
from modules import time_format

default_page_no = 1
default_num_perpage = 10
default_community_id = 0
default_post_id = 0
default_precent = 0.85


def service(request):
    if request.method == 'POST':
        type = request.form.get("type")
        if type == "publish":
            return publish_post(request)
        else:
            print "error request:", request
    elif request.method == 'GET':
        communit_id = request.args.get("community_id", 0)
        post_id = request.args.get("post_id", 0)
        if post_id != 0:
            return post_info(request)
        if communit_id != 0:
            return query_post_in_community(request)


def find_match_post(request):
    title = request.args.get("title")
    words = list(jieba.cut(title.strip(), cut_all=False))
    post_ids = []
    for word in words:
        data = db_model_inverted_index.select_by_word(word)
        if data != None:
            post_ids = list(set(post_ids + str(data.post_id).split(',')))
    if post_ids:
        # lcs
        dict_post = {}
        for id in post_ids:
            post = db_model_post.select_by_id(id)
            lcs_list, flag = mod_lcs.lcs(title, post.title)
            lcs_title = []
            lcs_title = mod_lcs.printLcs(flag, title, len(title), len(post.title), lcs_title)
            lcs_title = ''.join(lcs_title)
            # 匹配百分比
            percent = len(lcs_title.strip()) / float(len(title.strip()))
            dict_post[id] = percent  # dict:{'post_id':'percent',}
            # print 'id', id, 'lcs_title', lcs_title, 'percent', '%.2f' % percent
        # 按percent 由大到小排序
        dict_list = sorted(dict_post.items(), key=lambda e: e[1], reverse=True)
        # 从元组取值
        key = dict_list[0][0]
        value = dict_list[0][1]
        # 保留2位小数
        max_percent = round(value, 2)
        print 'key', key, 'value', value
        ids = []
        if max_percent > default_precent:
            for item in dict_list:  # 遍历元素是元组的集合
                if item[1] > default_precent:
                    ids.append(item[0])
                else:
                    break
        ids = ','.join(ids)
        paginate = db_model_post.select_by_ids(ids, default_page_no, default_num_perpage)
        post_list = []
        if True:
            for item in paginate.items:
                post_list.append(db_model_post.to_json(item))
        return post_list


def delete_post(request):
    param = json.loads(request.form.get('data'))
    post_id = param["post_id"]
    post = db_model_post.select_by_id(post_id)
    result = {}
    if post == None:
        result['code'] = 1
        print 'delete fail,post is not find'
    try:
        post.status = 1
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        post.last_update_time = update_time
        db_model_post.update(post)
        result['code'] = 0
    except Exception, e:
        result['code'] = 1
        print '删除失败'
    print 'delete post ', post_id

    return result


def publish_post(request):
    print "now publish post request"
    # insert to db
    title = request.form.get("title")
    content = request.form.get("content")
    path_type = 'post'
    content = mod_base64.base64_hander(content, path_type)
    create_user_id = request.form.get("create_user_id", 0)
    login_user = db_model_user.select_by_id(create_user_id)
    community_id = request.form.get("community_id", 0)
    floor_num = 0
    status = 0
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    last_update_time = create_time
    print 'title:', title, 'content:', content, "user_id:", create_user_id, "community_id:", community_id
    insert = db_model_post.insert(title, content, create_user_id, community_id, floor_num, create_time,
                                  last_update_time, status)
    print "now insert to db"

    print "record action of create post"
    action_content = {}
    action_content['post_id'] = insert.id
    db_model_action.insert(user_id=create_user_id, \
                           action_type_id=db_model_action_type.get_type_id('create_post'), \
                           action_detail_info=json.dumps(action_content, ensure_ascii=False), \
                           create_time=create_time)

    login_user.post_num = login_user.post_num + 1
    print "now update post_num to db", (login_user)

    # insert into inverted_index
    last_update_time = create_time
    # fenci
    words = list(jieba.cut(title.strip(), cut_all=False))
    print 'words length', len(words)
    for word in words:
        inverted_index = db_model_inverted_index.select_by_word(word)
        if inverted_index != None:
            post_id_list = str(inverted_index.post_id).split(',')
            post_id_list.append(str(insert.id))
            inverted_index.post_id = ','.join(post_id_list)
            inverted_index.last_update_time = last_update_time
            db_model_inverted_index.update(inverted_index)
        else:
            db_model_inverted_index.insert(word, insert.id, create_time, last_update_time)
    print 'now insert into inverted_index'

    # select db
    paginate = db_model_post.select_all_paging(default_page_no, default_num_perpage, community_id)
    print "now data:", paginate.items
    user_list = []
    for post in paginate.items:
        user = db_model_user.select_by_id(post.create_user_id)
        user_list.append(user)

    community = db_model_community.select_by_id(community_id)
    community.post_num = community.post_num + 1
    db_model_community.update(community)

    has_join = False
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        info = db_model_user_community.select_by_user_id_and_community_id(user_id=id, community_id=community_id)
        if info != None:
            has_join = True
    # return select value
    return paginate, user_list, community, has_join


def query_post_in_community(request):
    community_id = request.args.get("community_id", default_community_id)
    print " now query post in communit id:", community_id
    page_no = int(request.args.get("page_no", default_page_no))
    num_perpage = int(request.args.get("num_perpage", default_num_perpage))
    # select post indb
    paginate = db_model_post.select_all_paging(page_no, num_perpage, community_id)
    print "now data:", paginate.items

    user_list = []
    for post in paginate.items:
        user = db_model_user.select_by_id(post.create_user_id)
        user_list.append(user)

    has_join = False
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        info = db_model_user_community.select_by_user_id_and_community_id(user_id=user_id, community_id=community_id)
        print " query user_community:", "user_id:", user_id, "community_id:", community_id
        if info != None:
            has_join = True
    # select communit info in db
    community = db_model_community.select_by_id(community_id)
    # return select value
    paginate.items = formate_post_time(paginate.items)
    return paginate, user_list, community, has_join, page_no, len(paginate.items), num_perpage


def post_info(request):
    post_id = request.args.get("post_id", default_post_id)
    community_id = request.args.get("community_id", default_community_id)
    page_no = int(request.args.get("page_no", default_page_no))
    num_perpage = int(request.args.get("num_perpage", default_num_perpage))
    print " now query post info---- post_id:", post_id, " community_id: ", community_id, " page no:", page_no, " num_perpage:", num_perpage

    # select db
    post_data = db_model_post.select_by_id(post_id)
    post_user = db_model_user.select_by_id(post_data.create_user_id)
    reply_data = db_model_reply.select_paging_by_post_id(page_no, num_perpage, post_id)
    reply_user_list = []
    like_user_dict = {}
    for reply in reply_data.items:
        # add by lxx,like user start 2017-04-17
        like_user_dict[reply.id] = select_like_user(reply.id)
        # add by lxx,like user end
        user = db_model_user.select_by_id(reply.create_user_id)
        reply_user_list.append(user)
    community = db_model_community.select_by_id(community_id)
    best_reply = db_model_reply.select_best_by_post_id(post_id)
    if best_reply != None and best_reply.like_num < 3:
        best_reply = None
    best_reply_user = None
    if best_reply != None:
        best_reply_user = db_model_user.select_by_id(reply.create_user_id)
        like_user_dict[reply.id] = select_like_user(reply.id)
    print "post data:", post_data, "reply data:", reply_data

    def get_reply_like_count(reply):
        reply_id = reply.id
        count = db_model_reply_like_stat.get_reply_like_count(reply_id)
        return (reply_id, count)

    def is_reply_liked(reply):
        reply_id = reply.id
        if session.get('userinfo'):
            user_id = session.get('userinfo')['id']
            is_liked = db_model_reply_like_stat.is_reply_liked_by_user(reply_id, user_id)
            return (reply_id, is_liked)
        else:
            return (reply_id, False)

    liked_by_user = dict(map(is_reply_liked, reply_data.items))
    like_stats = dict(map(get_reply_like_count, reply_data.items))

    # return select value
    return post_data, post_user, reply_data, like_user_dict, reply_user_list, community, page_no, len( \
        reply_data.items), num_perpage, like_stats, liked_by_user, best_reply, best_reply_user


def select_good_post(request):
    page_no = int(request.args.get("no", default_page_no))
    num_perpage = int(request.args.get("size", default_num_perpage))

    # select db
    paginate = db_model_post.select_post_by_floor_num(page_no, num_perpage)
    post_list_new = formate_post_time(paginate.items)
    print len(post_list_new)
    return page_no, num_perpage, post_list_new


def formate_post_time(post_list):
    post_list_new = []
    for post_new in post_list:
        post_new.create_time = time_format.timestampFormat(post_new.create_time)
        post_list_new.append(post_new)
    print len(post_list_new)
    return post_list_new


def select_goodpost_all():
    max_number = 1000;
    paginate = db_model_post.select_post_by_floor_num(1, max_number)
    print paginate
    return len(paginate.items)


def select_like_user(reply_id):
    num_perpage = 10
    paginate = db_model_reply_like_stat.like_user(reply_id, default_page_no, num_perpage)
    user_list = []
    for item in paginate.items:
        user = db_model_user.select_by_id(item.user_id)
        user_list.append(db_model_user.to_json(user))
    return user_list
