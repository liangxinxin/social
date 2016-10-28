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

default_page_no = 1
default_num_perpage = 20
default_community_id = 0
default_post_id = 0

def service(request):
  print "enter do user_community  service"
  if request.method == 'POST':
    type=request.form.get("action")
    if type == "join":
      return user_join_community(request)
    elif type == "left":
      return user_left_community(request)
    else:
      print "error request:",request
  elif request.method == 'GET':
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

  #return select value
  community=db_model_community.select_by_id(id=community_id)
  community.user_num=community.user_num-1
  db_model_community.update(community)
  return community.user_num
#  rt=jsonify(result="succ",name=name,mobile=mobile) 
