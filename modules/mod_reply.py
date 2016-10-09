import sys
import pycurl
import cStringIO
import json
import urllib 
import urllib2 
import httplib 
import time 
from db_interface import db_model_post
from db_interface import db_model_reply

default_page_no = 1
default_num_perpage = 20
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
  #insert to db
  content = request.form.get("content")
  create_user_id = request.form.get("create_user_id",0)
  post_id = request.form.get("post_id",0)
  ISOTIMEFORMAT='%Y-%m-%d %X'
  create_time=time.strftime(ISOTIMEFORMAT,time.localtime())
  post_data = db_model_post.select_by_id(post_id)
  floor=post_data.floor_num+1
  post_data.floor_num+=1
  db_model_post.update(post_data)
  
  print 'content:',content,"user_id:",create_user_id,"post_id:",post_id
  db_model_reply.insert(content,create_user_id,post_id,floor,create_time)
  print "now insert to db"
  
  #select db
  paginate=db_model_reply.select_paging_by_post_id(default_page_no,default_num_perpage,post_id)
  print "now data:",paginate.items
  #return select value
  return post_data,paginate

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
