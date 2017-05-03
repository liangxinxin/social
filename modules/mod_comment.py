import json
import time

from flask import session
from db_interface import db_model_action
from db_interface import db_model_action_type
from db_interface import db_model_comment
from db_interface import db_model_message
from db_interface import db_model_reply
import time_format

default_comment_id = 0
default_reply_id =0
default_page_no=1
default_num_perpage=5
def service(request):
  if request.method == 'POST':
    type = request.form.get("type")
    print 'post'
    if type == 'publish':
        return publish_comment(request)
    elif type == 'delete':
        return delete_comment(request)

  elif request.method == 'GET':
    type = request.args.get("type")
    if type == 'query':
        print " request is:",request
        return query_by_reply_id(request)



def query_by_reply_id(request):
    reply_id = request.args.get('reply_id',default_reply_id)
    page_no =int(request.args.get("page_no", default_page_no))
    num_perpage = int(request.args.get("num_perpage", default_num_perpage))
    paginate = db_model_comment.select_by_reply_id(reply_id,page_no,num_perpage)
    json_comment_list =[]
    for comment in paginate.items:
        comment =db_model_comment.to_json(comment)
        json_comment_list.append(comment)
    paginate.items = json_comment_list
    return paginate

def publish_comment(request):
    print ' publish comment'
    create_user_id = 0
    result={}
    if session.get('userinfo')!=None:
        create_user_id = (int)(session.get('userinfo')['id'])
        reply_id = request.form.get('reply_id')
        parent_id = int(request.form.get('comment_id', 0))
        community_id = request.form.get('community_id')
        content = request.form.get('content')
        reply = db_model_reply.select_by_id(reply_id)
        if reply == None:
            print 'reply is none'
            result['code'] = 1
            result['message'] = 'reply is none'
            return result
        to_user_id = 0
        if parent_id>0:
            comment = db_model_comment.select_by_id(parent_id)
            to_user_id = comment.create_user_id
        else:
            to_user_id = reply.create_user_id
        post_id = reply.post_id
        floor = reply.floor_num+1
        status =0
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        last_upate_time = create_time
        if int(parent_id)==0:
            parent_id=None
        data = db_model_comment.insert(content,create_user_id,reply_id,community_id,post_id,to_user_id,parent_id,floor,create_time,status,last_upate_time)
        db_model_reply.update_floor_num(reply_id, floor)
        if create_user_id != to_user_id:
            db_model_message.insert_comment_message(data.id)

        print "record action of create post"
        action_content={}
        action_content['comment_id']=data.id
        db_model_action.insert(user_id=create_user_id, \
                               action_type_id=db_model_action_type.get_type_id('create_comment'), \
                               action_detail_info=json.dumps(action_content, ensure_ascii = False), \
                               create_time=create_time)
        data.create_time = time_format.timestampFormat(data.create_time)
        data = db_model_comment.to_json(data)
        result['code'] = 0
        result['message'] = 'success'
        result['comment'] = data
        return result

def delete_comment(request):
    result = {}
    #delete
    comment_id = request.form.get('comment_id')
    print 'do delete comment'
    comment = db_model_comment.select_by_id(comment_id)
    if comment == None:
        result['code']=1
        return result
    comment.status = 1
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    last_update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    comment.last_upate_time = last_update_time
    result['code'] = 0
    try:
        db_model_comment.update_comment(comment)
        reply = db_model_reply.select_by_id(comment.reply_id)
        if reply.floor_num>0:
            reply.floor_num = reply.floor_num - 1
        reply.last_update_time = last_update_time
        db_model_reply.update(reply)

    except :
        result['code'] =1
    return result