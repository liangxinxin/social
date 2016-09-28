import sys
import pycurl
import cStringIO
import json
import urllib 
import urllib2 
import httplib 
import time 
from db_interface import db_model_post

default_page_no = 1
default_num_perpage = 20
default_community_id = 1

def service(request):
  if request.method == 'POST':
    type=request.form.get("type")
    if type == "publish":
      return publish_post(request)
    else:
      print "error request:",request
  elif request.method == 'GET':
    return query_post_in_community(request)

def publish_post(request):
  print "now publish post request"
  #insert to db
  title = request.form.get("title")
  content = request.form.get("content")
  create_user_id = request.form.get("create_user_id",0)
  community_id = request.form.get("community_id",0)
  floor_num=0
  ISOTIMEFORMAT='%Y-%m-%d %X'
  create_time=time.strftime(ISOTIMEFORMAT,time.localtime())
  last_update_time=create_time
  print 'title:',title,'content:',content,"user_id:",create_user_id,"community_id:",community_id
  db_model_post.insert(title,content,create_user_id,community_id,floor_num,create_time,last_update_time)
  print "now insert to db"
  
  #select db
  paginate=db_model_post.select_all_paging(default_page_no,default_num_perpage,community_id)
  print "now data:",paginate.items
  #return select value
  return paginate,community_id 

def query_post_in_community(request):
  community_id = request.args.get("id",default_community_id)
  print " now query post in communit id:",community_id
  page_no = request.args.get("page_no",default_page_no)
  num_perpage = request.args.get("num_perpage",default_num_perpage)
  #select db
  paginate=db_model_post.select_all_paging(page_no,num_perpage,community_id)
  print "now data:",paginate.items

  #return select value
  return paginate,community_id
