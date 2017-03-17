# coding=utf-8
import sys
import pycurl
import cStringIO
import json
import urllib
import urllib2
import httplib
import time
import time_format
from flask import session
from db_interface import db_model_user
from db_interface import db_model_community
from db_interface import db_model_post
from db_interface import db_model_reply
from db_interface import db_model_reply_like_stat
from db_interface import db_model_message

default_page_no = 1
default_num_perpage = 10
default_community_id = 1


def service(request):
    if request.method == 'POST':
        type = request.form.get("type")
        if type == "publish":
            return publish_reply(request)
        else:
            print "error request:", request
    elif request.method == 'GET':
        print "hehe,the request is:", request


# communit_id=request.args.get("community_id",0)
#    post_id=request.args.get("post_id",0)
#    if communit_id != 0:
#      return query_post_in_community(request)
#    if post_id != 0:
#      return post_info(request)

def publish_reply(request):
    print "publish reply request"
    content = request.form.get("content")
    create_user_id = long(request.form.get("create_user_id", 0))
    post_id = request.form.get("post_id", 0)
    community_id = request.form.get("community_id", 0)

    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    post_data = db_model_post.select_by_id(post_id)
    floor = post_data.floor_num + 1
    post_data.floor_num += 1
    db_model_post.update(post_data)

    floor_num = 0
    like_num = 0
    post_user = db_model_user.select_by_id(post_data.create_user_id)

    print 'create reply--- content:', content, "user_id:", create_user_id, "post_id:", post_id, "community_id", community_id
    # insert to db
    db_model_reply.insert(content, create_user_id, post_id, floor, floor_num, like_num, create_time)
    reply = db_model_reply.select_by_create_user_and_post_and_floor(create_user_id, post_id, floor)
    if reply != None and (create_user_id != post_data.create_user_id):
        db_model_message.insert_reply_post(create_user_id, post_id, reply.id)
    print "now insert to db"

    # select db
    paginate = db_model_reply.select_paging_by_post_id(default_page_no, default_num_perpage, post_id)
    print "now data:", paginate.items
    reply_user_list = []
    for reply in paginate.items:
        user = db_model_user.select_by_id(reply.create_user_id)
        reply_user_list.append(user)

    community = db_model_community.select_by_id(community_id)

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

    liked_by_user = dict(map(is_reply_liked, paginate.items))
    like_stats = dict(map(get_reply_like_count, paginate.items))
    # return select value
    return post_data, post_user, paginate, reply_user_list, community, default_page_no, len(
        paginate.items), default_num_perpage, like_stats, liked_by_user


def reply_like_changed(request):
    if session.get('userinfo'):
        print "user's info-------------------\n", session.get('userinfo')
        user_id = session.get('userinfo')['id']
        reply_id = request.args.get("replyid")
        mod_type = request.args.get("modtype")
        reply = db_model_reply.select_by_id(reply_id)
        if mod_type == "add":
            ISOTIMEFORMAT = '%Y-%m-%d %X'
            create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
            db_model_reply_like_stat.insert(reply_id, user_id, create_time)
            db_model_message.insert_praise_reply(user_id, reply_id)
            reply.like_num += 1
            db_model_reply.update_like_num(reply_id, reply.like_num)
        else:
            db_model_reply_like_stat.remove(reply_id, user_id)
            reply.like_num -= 1
            db_model_reply.update_like_num(reply_id, reply.like_num)


def get_reply_by_post(request):
    login_user_id = 0
    if session.get('userinfo'):
        login_user_id = session.get('userinfo')['id']

    post_id = request.args.get("post_id")
    post = db_model_post.select_by_id(post_id)
    page_no = int(request.args.get("no", default_page_no))
    num_perpage = int(request.args.get("size", default_num_perpage))
    paginate = db_model_reply.select_paging_by_post_id(page_no, num_perpage, post_id)
    reply_list=[]
    for reply in paginate.items:
        is_like = db_model_reply_like_stat.is_reply_liked_by_user(reply.id, login_user_id)
        reply.create_time =time_format.timestampFormat(reply.create_time)
        reply = db_model_reply.to_json(reply)
        reply['is_like']=is_like
        reply_list.append(reply)
    return reply_list,page_no,num_perpage,paginate.total



def publish_reply_in_UserInfo(request):
    data = json.loads(request.form.get("data"))
    content = data["content"]
    create_user_id = long(data["create_user_id"])
    post_id = data["post_id"]
    community_id = request.args.get("community_id", 0)

    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    post_data = db_model_post.select_by_id(post_id)
    floor = post_data.floor_num + 1
    post_data.floor_num += 1
    db_model_post.update(post_data)
    floor_num = 0
    like_num = 0
    is_like = False
    print 'create reply--- content:', content, "user_id:", create_user_id, "post_id:", post_id, "community_id", community_id
    # insert to db
    db_model_reply.insert(content, create_user_id, post_id, floor, floor_num, like_num, create_time)
    reply = db_model_reply.select_by_create_user_and_post_and_floor(create_user_id, post_id, floor)
    if reply != None and (create_user_id != post_data.create_user_id):
        db_model_message.insert_reply_post(create_user_id, post_id, reply.id)
    print "now insert to db"
    reply.create_time= time_format.timestampFormat(reply.create_time)
    reply= db_model_reply.to_json(reply)
    return reply, post_data.floor_num
# def query_post_in_community(request):
#  community_id = request.args.get("community_id",default_community_id)
#  print " now query post in communit id:",community_id
#  page_no = request.args.get("page_no",default_page_no)
#  num_perpage = request.args.get("num_perpage",default_num_perpage)
#  #select db
#  paginate=db_model_post.select_all_paging(page_no,num_perpage,community_id)
#  print "now data:",paginate.items
#
#  #return select value
#  return paginate,community_id

# def post_info(request):
#  post_id = request.args.get("post_id",default_community_id)
#  print " now query post in communit id:",post_id
#  page_no = request.args.get("page_no",default_page_no)
#  num_perpage = request.args.get("num_perpage",default_num_perpage)
#  #select db
#  post_data=db_model_post.select_by_id(post_id)
#  reply_data=db_model_reply.select_paging_by_post_id(post_id,page_no,num_perpage)
#  print "now data:",post_data
#
#  #return select value
#  return post_data,reply_data
