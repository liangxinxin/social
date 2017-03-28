import sys
import pycurl
import cStringIO
import json
import urllib
import urllib2
import httplib
import time
from flask import session
from db_interface import db_model_user
from db_interface import db_model_community
from db_interface import db_model_user_community
from db_interface import db_model_post
from db_interface import db_model_reply
from db_interface import db_model_reply_like_stat
from modules import time_format

default_page_no = 1
default_num_perpage = 10
default_community_id = 0
default_post_id = 0


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


def publish_post(request):
    print "now publish post request"
    # insert to db
    title = request.form.get("title")
    content = request.form.get("content")
    create_user_id = request.form.get("create_user_id", 0)
    login_user = db_model_user.select_by_id(create_user_id)
    community_id = request.form.get("community_id", 0)
    floor_num = 0
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    last_update_time = create_time
    print 'title:', title, 'content:', content, "user_id:", create_user_id, "community_id:", community_id
    db_model_post.insert(title, content, create_user_id, community_id, floor_num, create_time, last_update_time)
    print "now insert to db"

    login_user.post_num = login_user.post_num + 1
    print "now update post_num to db",(login_user)

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
    for reply in reply_data.items:
        user = db_model_user.select_by_id(reply.create_user_id)
        reply_user_list.append(user)
    community = db_model_community.select_by_id(community_id)
    best_reply = db_model_reply.select_best_by_post_id(post_id)
    if best_reply.like_num < 3:
      best_reply=None
    best_reply_user=None
    if best_reply != None:
      best_reply_user=db_model_user.select_by_id(reply.create_user_id)
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
    return post_data, post_user, reply_data, reply_user_list, community, page_no, len(\
        reply_data.items), num_perpage, like_stats, liked_by_user,best_reply,best_reply_user


def select_good_post(request):
    page_no = int(request.args.get("no", default_page_no))
    num_perpage = int(request.args.get("size", default_num_perpage))

    # select db
    paginate = db_model_post.select_post_by_floor_num(page_no, num_perpage)
    post_list_new=formate_post_time(paginate.items)
    print len(post_list_new)
    return page_no,num_perpage,post_list_new


def formate_post_time(post_list):
    post_list_new=[]
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
