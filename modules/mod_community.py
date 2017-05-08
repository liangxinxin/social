#coding=utf8
import json
import time


from flask import session

from db_interface import db_model_action
from db_interface import db_model_action_type
from db_interface import db_model_community
from db_interface import db_model_post
from db_interface import db_model_user_community
import  time_format

default_page_no = 1
default_num_perpage = 20
hot_num_perage = 4
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
    elif service_type == 'update':
      return  update_community(request)

  elif request.method == 'GET':
    type = request.args.get("type")
    print 'type',type
    if type =='commend_community':
      return select_hot_commend_community(request)
    elif type =='query':
      return get_community_info(request)
    else:
      return query_community(request)



def update_community(request):
    id = request.form.get("id")
    name = request.form.get("name")
    desc = request.form.get("desc")
    community = db_model_community.select_by_id(id)
    result={}
    try:
      if community :
        community.name = name
        community.describe = desc
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        community.create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        db_model_community.update(community)
        result['code'] = 0
        result['message'] = 'success'
      else:
        result['code'] = 1
        result['message'] = 'community is null'
    except Exception,e:
      print Exception,":",e
      result['code'] = 1
      result['message'] = 'fail'
    return result



def query_community(request):
  print " now query community by name!"
  name = request.form.get("name","")
  page_no = request.form.get("page_no",default_page_no)
  num_perpage = request.form.get("num_perpage",default_num_perpage)

  #select db
  community_name=name
  index=community_name.find('岛'.decode('utf8'))
  if index+1 == len(community_name):
    community_name=community_name[:index]
  print community_name,name
  paginate=None
  paginate=db_model_community.select_by_name_paging(community_name,page_no,num_perpage)

  #return select value
  return paginate,name,community_name

def get_community_info(request):
  print " now query community info by id!"
  id = request.args.get("id",default_community_id)
  community=db_model_community.select_by_id(id)
  has_join = False
  if session.get('userinfo'):
    user_id = session.get('userinfo')['id']
    info = db_model_user_community.select_by_user_id_and_community_id(user_id=user_id, community_id=id)
    if info != None:
      has_join = True
  return community,has_join

def publish_community(request):
  result = {}
  if session.get('userinfo'):
    create_user_id = session.get('userinfo')['id']
    print "publish community request"
    #insert to db
    name = request.form.get("name","default")
    describe = request.form.get("describe","finance home")
    head_img_url = request.form.get("head_img_url","https://img3.doubanio.com/icon/g35417-1.jpg")
    try:
      ISOTIMEFORMAT='%Y-%m-%d %X'
      create_time=time.strftime(ISOTIMEFORMAT,time.localtime())
      #db_model_community.insert(title,content,create_user_id,community_id,floor_num,create_time,last_update_time)
      print "now insert new community to db"
      data=db_model_community.insert(name=name,user_num=1,post_num=0,describe=describe,head_img_url=head_img_url,create_user_id=create_user_id,create_time=create_time)
      #select db
      if data == None:
        result['code'] = 1
        result['message'] = 'fail'
        result['data'] = ''
        return result
      else:
        db_model_user_community.insert(create_user_id, data.id, create_time)
        data = db_model_community.to_json(data)
      print "community id:",data['id']
      print "record action of create community"
      action_content={}
      action_content['user_id']=int(create_user_id)
      action_content['community_id']=int(data['id'])
      db_model_action.insert(user_id=create_user_id,\
             action_type_id=db_model_action_type.get_type_id('create_community'),\
             action_detail_info=json.dumps(action_content, ensure_ascii = False),\
             create_time=create_time)
      result['code']= 0
      result['data'] = data
      result['message']='success'
    except Exception,e:
      print e
      result['code'] = 1
      result['message'] = 'fail'
      result['data'] = ''
  else:
    result['code'] = 1
    result['message'] = 'fail'
    result['data'] = ''
    print 'user is null'
  # paginate=db_model_post.select_all_paging(default_page_no,default_num_perpage,data.id)
  # print "now data:",paginate.items,len(paginate.items)
  #has_join=True
  #return paginate,data,has_join
  #return select value
  return result

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
  

def select_hot_commend_community(request):
    current_community_id = int(request.args.get('community_id',0))
    comm_ids = [current_community_id]
    page_no = request.args.get('page_no',default_page_no)
    num_page = request.args.get('num_page',hot_num_perage)
    commend_list =[]
    if session.get('userinfo') and current_community_id:# commend_community
      user_id = session.get('userinfo')['id']
      #select join communty
      community_list = db_model_user_community.select_all_join_community_id(user_id)
      if community_list:
        map(lambda x: int(x), community_list[0])
        comm_ids = list(set(comm_ids+list(map(lambda x: int(x), community_list[0]))))
        paginate = db_model_community.select_commend_community(page_no,hot_num_perage,comm_ids)
      else:
        paginate = db_model_community.select_by_user_num(default_page_no, hot_num_perage, current_community_id)
    else:# hot_community
      paginate = db_model_community.select_by_user_num(default_page_no,hot_num_perage,current_community_id)
    commend_list = paginate.items
    commend_list_new = []
    for item in commend_list:
      commend_list_new.append(db_model_community.to_json(item))
    return page_no,num_page,commend_list_new



def find_match_community(request):
  name = request.args.get('name')
  num_perpage=10
  paginate = db_model_community.select_by_name_paging(name,default_page_no,num_perpage)
  comm_list = []
  for item in paginate.items:
    comm_list.append(db_model_community.to_json(item))
  return comm_list