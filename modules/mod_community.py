import sys
import pycurl
import cStringIO
import json
import urllib 
import urllib2 
import httplib 
import time 
from db_interface import db_model_post
from db_interface import db_model_community

default_page_no = 1
default_num_perpage = 20
default_community_id = 1

def service(request):
  if request.method == 'POST':
    print "post!"
    service_type=request.form.get("type")
    print service_type
    if service_type == "query":
      return query_community(request)
    elif service_type == "publish":
      return publish_community(request)
  elif request.method == 'GET':
    print "get!"
    return query_community(request)

def query_community(request):
  print " now query community by name!"
  name = request.form.get("name"," ")
  page_no = request.form.get("page_no",default_page_no)
  num_perpage = request.form.get("num_perpage",default_num_perpage)

  #select db
  paginate=None
  paginate=db_model_community.select_by_name_paging(name,page_no,num_perpage)

  #return select value
  return paginate,name 

def publish_community(request):
  print "publish community request"
  #insert to db
  name = request.form.get("name","default")
  describe = request.form.get("describe","finance home")
  create_user_id = request.form.get("create_user_id",0)
  head_img_url = request.form.get("head_img_url","https://img3.doubanio.com/icon/g35417-1.jpg")
  ISOTIMEFORMAT='%Y-%m-%d %X'
  create_time=time.strftime(ISOTIMEFORMAT,time.localtime())
  #db_model_community.insert(title,content,create_user_id,community_id,floor_num,create_time,last_update_time)
  db_model_community.insert(name=name,user_num=1,post_num=0,describe=describe,head_img_url=head_img_url,create_user_id=create_user_id,create_time=create_time)
  print "now insert to db"
  
  #select db
  data=db_model_community.select_by_name_equal(name)
  print "community id:",data.id
  if data == None:
    return None,0
  paginate=db_model_post.select_all_paging(default_page_no,default_num_perpage,data.id)
  print "now data:",paginate.items,len(paginate.items)
  return paginate,data.id 
  #return select value