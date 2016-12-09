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
from db_interface import db_model_post
from db_interface import db_model_reply
from db_interface import db_model_reply_like_stat

default_page_no = 1
default_num_perpage = 15 
default_community_id = 1

def service(request):
  if request.method == 'POST':
    type=request.form.get("type")
    if type == "publish":
      return publish_reply(request)
    else:
      print "error request:",request
  elif request.method == 'GET':
    print "hehe,the request is:",request
#    communit_id=request.args.get("community_id",0)
#    post_id=request.args.get("post_id",0)
#    if communit_id != 0:
#      return query_post_in_community(request)
#    if post_id != 0:
#      return post_info(request)

def publish_reply(request):
  print "publish reply request"
  content = request.form.get("content")
  create_user_id = request.form.get("create_user_id",0)
  post_id = request.form.get("post_id",0)
  community_id = request.form.get("community_id",0)

  ISOTIMEFORMAT='%Y-%m-%d %X'
  create_time=time.strftime(ISOTIMEFORMAT,time.localtime())
  post_data = db_model_post.select_by_id(post_id)
  floor=post_data.floor_num+1
  post_data.floor_num+=1
  db_model_post.update(post_data)
  
  post_user=db_model_user.select_by_id(post_data.create_user_id)

  print 'create reply--- content:',content,"user_id:",create_user_id,"post_id:",post_id,"community_id",community_id
  #insert to db
  db_model_reply.insert(content,create_user_id,post_id,floor,create_time)
  print "now insert to db"
  
  #select db
  paginate=db_model_reply.select_paging_by_post_id(default_page_no,default_num_perpage,post_id)
  print "now data:",paginate.items
  reply_user_list=[]
  for reply in paginate.items:
    user = db_model_user.select_by_id(reply.create_user_id)
    reply_user_list.append(user)

  community = db_model_community.select_by_id(community_id)
  #return select value
  return post_data,post_user,paginate,reply_user_list,community,default_page_no,len(paginate.items),default_num_perpage

def reply_like_changed(request):
  if session.get('userinfo'):
    user_id = session.get('userinfo')['id']
    reply_id= request.args.get("replyid")
    mod_type= request.args.get("modtype")
    if mod_type == "add":
      ISOTIMEFORMAT='%Y-%m-%d %X'
      create_time=time.strftime(ISOTIMEFORMAT,time.localtime())
      db_model_reply_like_stat.insert(reply_id, user_id, create_time)
    else:
      db_model_reply_like_stat.remove(reply_id, user_id)
    

#def query_post_in_community(request):
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

#def post_info(request):
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
