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

default_page_no = 1
default_num_perpage = 20
default_community_id = 0
default_post_id = 0

def service(request):
  print "enter do user create service"
  if request.method == 'POST':
    type=request.form.get("type")
    if type == "publish":
      return create_user(request)
    else:
      print "error request:",request
  elif request.method == 'GET':
    user_id=request.args.get("user_id",0)
    if user_id != 0:
      return query_user_info(request)

def create_user(request):
  print "now create new user request"
  #insert to db
  name = request.form.get("name")
  password = request.form.get("password")
  mobile = request.form.get("mobile",0)
  ISOTIMEFORMAT='%Y-%m-%d %X'
  create_time=time.strftime(ISOTIMEFORMAT,time.localtime())
  print 'name:',name,'mobile:',mobile
  print "now insert to db"
  db_model_user.insert(name=name,password=password,mobile=mobile)

  #return select value
  user=db_model_user.select_by_name_and_password_and_mobile(name=name,password=password,mobile=mobile)
  if user != None:
    session['userinfo'] = {'name':user.name, 'id':user.id}
  return    
#  rt=jsonify(result="succ",name=name,mobile=mobile) 

def query_user_info(request):
  user_id=request.args.get("user_id")
  user_info =db_model_user.select_by_id(user_id) 
  return user_info
