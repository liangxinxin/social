from flask import session
import sys
import pycurl
import cStringIO
import json
import urllib 
import urllib2 
import httplib 
import time 
from db_interface import db_model_user
from db_interface import db_model_community
from db_interface import db_model_user_community
from db_interface import db_model_action
from db_interface import db_model_action_type

default_page_no = 1
default_num_perpage = 20
default_community_id = 0
default_post_id = 0

def service(request):
  print "enter do user_community  service"
  if request.method == 'POST':
    type=request.form.get("type")
    if type == "join":
      return user_join_community(request)
    elif type == "left":
      return user_left_community(request)
    else:
      print "error request:",request
  elif request.method == 'GET':
    type = request.args.get("type")
    if type == 'joined':
      return find_community_user_join(request)
    else:
      return "to do in soon after" 

def user_join_community(request):
  print "now deal user join community!"
  #insert to db
  user_id = int(request.form.get("user_id"))
  community_id = int(request.form.get("community_id"))
  ISOTIMEFORMAT='%Y-%m-%d %X'
  create_time=time.strftime(ISOTIMEFORMAT,time.localtime())
  print 'uid:',user_id,'cid:',community_id
  print "now insert to db"
  db_model_user_community.insert(user_id=user_id,community_id=community_id,create_time=create_time)
  print "record action of user join community"
  action_content={}
  action_content['user_id']=user_id
  action_content['community_id']=community_id
  db_model_action.insert(user_id=user_id,\
         action_type_id=db_model_action_type.get_type_id('join_community'),\
         action_detail_info=json.dumps(action_content, ensure_ascii = False),\
         create_time=create_time)
  
  #return select value
  community=db_model_community.select_by_id(id=community_id)
  community.user_num=community.user_num+1
  db_model_community.update(community)
  return community.user_num
#  rt=jsonify(result="succ",name=name,mobile=mobile) 

def user_left_community(request):
  print "now deal user join community!"
  #insert to db
  user_id = request.form.get("user_id")
  community_id = request.form.get("community_id")
  ISOTIMEFORMAT='%Y-%m-%d %X'
  create_time=time.strftime(ISOTIMEFORMAT,time.localtime())
  print 'uid:',user_id,'cid:',community_id
  print "now insert to db"
  info=db_model_user_community.select_by_user_id_and_community_id(user_id=user_id,community_id=community_id)
  if info != None:
    db_model_user_community.delete(info.id)

  print "record action of user left community"
  action_content={}
  action_content['user_id']=user_id
  action_content['community_id']=community_id
  db_model_action.insert(user_id=user_id,\
         action_type_id=db_model_action_type.get_type_id('left_community'),\
         action_detail_info=json.dumps(action_content, ensure_ascii = False),\
         create_time=create_time)

  #return select value
  community=db_model_community.select_by_id(id=community_id)
  community.user_num=community.user_num-1
  db_model_community.update(community)
  return community.user_num
#  rt=jsonify(result="succ",name=name,mobile=mobile)


def find_community_user_join(request):
   community_list = []
   user_id = request.args.get("user_id")
   page_no = int(request.args.get('no',default_page_no))
   num_perpage = int(request.args.get('size',default_num_perpage))
   data = db_model_user_community.select_user_joined_community(user_id,page_no,num_perpage)
   totalCount = data.total
   totalPages = data.pages
   for item in data.items:
    community = db_model_community.select_by_id(item.community_id)
    community_list.append(db_model_community.to_json(community))
   return community_list,page_no,num_perpage,totalCount,totalPages

def user_has_join_community(community_id):
  has_join = False
  if session.get('userinfo'):
    user_id = session.get('userinfo')['id']
    info = db_model_user_community.select_by_user_id_and_community_id(user_id=user_id, community_id=community_id)
    if info != None:
      has_join = True 
  print "user:",user_id,"community:",community_id," join:",has_join
  return has_join
