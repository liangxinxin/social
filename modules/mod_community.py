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
from db_interface import db_model_action
from db_interface import db_model_action_type

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
  name = request.form.get("name","")
  page_no = request.form.get("page_no",default_page_no)
  num_perpage = request.form.get("num_perpage",default_num_perpage)

  #select db
  paginate=None
  paginate=db_model_community.select_by_name_paging(name,page_no,num_perpage)

  #return select value
  return paginate,name

def get_community_info(request):
  print " now query community info by id!"
  id = request.args.get("id",default_community_id)
  community=db_model_community.select_by_id(id)

  return community

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
  print "now insert new community to db"
  data=db_model_community.insert(name=name,user_num=1,post_num=0,describe=describe,head_img_url=head_img_url,create_user_id=create_user_id,create_time=create_time)
  #select db
  if data == None:
    return None,0
  print "community id:",data.id
  
  print "record action of create community"
  action_content={}
  action_content['user_id']=create_user_id
  action_content['community_id']=data.id
  db_model_action.insert(user_id=create_user_id,\
         action_type_id=db_model_action_type.get_type_id('create_community'),\
         action_detail_info=json.dumps(action_content, ensure_ascii = False),\
         create_time=create_time)  
 
  paginate=db_model_post.select_all_paging(default_page_no,default_num_perpage,data.id)
  print "now data:",paginate.items,len(paginate.items)
  has_join=True
  return paginate,data,has_join 
  #return select value

def get_default_communities(page_no, page_size):
  print "get default communities:"
  paginate = db_model_community.select_all_paging(page_no, page_size)
  return paginate.items

def get_hot_communities_total_num():
  max_number = 1000;
  data = db_model_community.select_all_paging(1, max_number)
  if data == None:
    return 0
  else:
    return len(data.items)
  
    
def select_good_community(request):
   # page_no = int(request.args.get("no", default_page_no))
   # num_perpage = int(request.args.get("size", default_num_perpage))
    page_no = 1
    num_perpage=4 

    # select db
    paginate = db_model_community.select_by_user_num(page_no, num_perpage)
    return page_no,num_perpage,paginate.items 

