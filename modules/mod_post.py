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
from  db_interface import db_model_comment
from modules import mod_base64
from modules import mod_lcs
from modules import time_format
from Logger import *
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
            Logger.infoLogger.error('error request:%s',request)
    elif request.method == 'GET':
        type = request.args.get("type")
        if type =='getpost':
            return query_post_in_community(request)
        elif type=='postInfo':
            return post_info(request)
        elif type == 'hot':
            return select_good_post(request)
        elif type == 'delete':
            return delete_post(request)
        else:
            return select_goodpost_num()


def find_match_post(request):
    title = request.args.get("title")
    words = list(jieba.cut(title.strip(), cut_all=False))
    post_ids = []
    for word in words:
        data = db_model_inverted_index.select_by_word(word)
        if data:
            post_ids = list(set(post_ids + str(data.post_id).split(',')))
    if post_ids:
        # lcs
        dict_post = {}
        for id in post_ids:
            post = db_model_post.select_by_id(id)
            if post:
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
        Logger.infoLogger.info('key: %s,value:%s', key, value)
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
    post_id = request.form.get("post_id")
    post = db_model_post.select_by_id(post_id)
    result = {}
    if post is None:
        result['code'] = 1
        result['message'] ='delete fail,post is not find'
        return result
    try:
        post.status = 1
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        post.last_update_time = update_time
        db_model_post.update(post)
        # to do 删除分词的postid
        inverted_index_list = db_model_inverted_index.select_by_post_id(post.id)
        for item in inverted_index_list:
            post_id_list = item.post_id.split(',')
            post_id_list.remove(str(post.id))
            item.post_id = ','.join(post_id_list)
            item.last_update_time = update_time
            db_model_inverted_index.update(item)
        Logger.infoLogger.info('delete inverted_index success!')
        community = db_model_community.select_by_id(post.community_id)
        # update community post_num
        community.post_num -= 1
        db_model_community.update(community)
        # dele reply,comment
        for reply in post.replys:
            reply.status =1
            for comment in reply.comments:
                comment.status =1
                db_model_comment.update_comment(comment)
            db_model_reply.update(reply)
        result['code'] = 0
        result['message'] = 'delete success !'
    except Exception, e:
        result['code'] = 1
        result['message'] = 'delete Exception !'
        Logger.infoLogger.error('Exception:%s',e)
    Logger.infoLogger.info('delete post:%s', post_id)

    return result


def publish_post(request):
    Logger.infoLogger.info('now publish post request')
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
    Logger.infoLogger.info('title:%s,content:%s,user_id:%s,community_id:%s',title,content,create_user_id,community_id)
    insert = db_model_post.insert(title, content, create_user_id, community_id, floor_num, create_time,
                                  last_update_time, status)
    Logger.infoLogger.info('now insert to db')
    Logger.infoLogger.info('record action of create post')
    action_content = {'post_id': insert.id}
    db_model_action.insert(user_id=create_user_id, \
                           action_type_id=db_model_action_type.get_type_id('create_post'), \
                           action_detail_info=json.dumps(action_content, ensure_ascii=False), \
                           create_time=create_time)

    login_user.post_num += 1
    Logger.infoLogger.info('now update post_num to db %s',login_user)

    # insert into inverted_index
    last_update_time = create_time
    # fenci
    words = list(jieba.cut(title.strip(), cut_all=False))
    Logger.infoLogger.info('words length %s',len(words))
    for word in words:
        inverted_index = db_model_inverted_index.select_by_word(word)
        if inverted_index :
            post_id_list = str(inverted_index.post_id).split(',')
            post_id_list.append(str(insert.id))
            inverted_index.post_id = ','.join(post_id_list)
            inverted_index.last_update_time = last_update_time
            db_model_inverted_index.update(inverted_index)
        else:
            db_model_inverted_index.insert(word, insert.id, create_time, last_update_time)
    Logger.infoLogger.info('now insert into inverted_index')

    # select db
    paginate = db_model_post.select_all_paging(default_page_no, default_num_perpage, community_id)
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
        info = db_model_user_community.select_by_user_id_and_community_id(user_id=user_id, community_id=community_id)
        if info:
            has_join = True
    # return select value
    return paginate, user_list, community, has_join


def query_post_in_community(request):
    community_id = request.args.get("community_id", default_community_id)
    Logger.infoLogger.info('now query post in communit id:%s',community_id)
    page_no = int(request.args.get("page_no", default_page_no))
    num_perpage = int(request.args.get("num_perpage", default_num_perpage))
    # select post indb
    paginate = db_model_post.select_all_paging(page_no, num_perpage, community_id)
    # return select value
    paginate.items = formate_post_time(paginate.items)
    return paginate, page_no, num_perpage


def post_info(request):
    post_id = request.args.get("id", default_post_id)
    # select db
    post= db_model_post.select_by_id(post_id)
    if post:
        post.create_time = time_format.timestampFormat(post.create_time)
    return post


def select_good_post(request):
    max_number = 1000;
    page_no = int(request.args.get("page_no", default_page_no))
    num_perpage = int(request.args.get("num_perpage", default_num_perpage))
    if page_no > (max_number/num_perpage):
        page_no = (max_number/num_perpage)
    # select db
    paginate = db_model_post.select_post_by_floor_num(page_no, num_perpage)
    post_list = formate_post_time(paginate.items)
    if paginate.total>max_number:
        total =max_number
    else:
        total = paginate.total
    return page_no, num_perpage, post_list,total


def formate_post_time(post_list):
    post_list_new = []
    for post_new in post_list:
        post_new.create_time = time_format.timestampFormat(post_new.create_time)
        post_list_new.append(db_model_post.to_json(post_new))
    return post_list_new


def select_goodpost_num():
    max_number = 1000;
    count = db_model_post.select_post_num()
    if count>max_number:
        count =max_number
    return count



