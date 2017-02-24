from db_interface import db_model_user
from db_interface import db_model_comment
from db_interface import db_model_reply
from db_interface import db_model_message
import time
from flask import session
default_comment_id = 0
default_reply_id =0
default_page_no=1
default_num_perpage=5

def service(request):
  if request.method == 'POST':
    print 'post'
    return publish_comment(request);

  elif request.method == 'GET':
    print " request is:",request
    query_by_reply_id(request)



def query_by_reply_id(request):
    reply_id = request.args.get('replyid',default_reply_id)
    page_no =int(request.args.get("page_no", default_page_no))
    paginate = db_model_comment.select_by_reply_id(reply_id,page_no,default_num_perpage)
    comment_list = paginate.items
    json_comment_list =[]
    for comment in paginate.items:
        #comment.user = db_model_user.to_json(comment.user)
        comment =db_model_comment.to_json(comment)
        json_comment_list.append(comment)
    paginate.items = json_comment_list
    return paginate

def publish_comment(request):
    print ' publish comment'
    create_user_id = 0
    if session.get('userinfo')!=None:
        create_user_id = (int)(session.get('userinfo')['id'])
    reply_id = request.args.get('replyid', default_reply_id)
    community_id = request.args.get('communityid')
    post_id = request.args.get('postid')
    to_user_id =request.args.get('touid')
    parent_id = request.args.get('parentid', default_comment_id)
    content = request.args.get('content')
    reply = db_model_reply.select_by_id(reply_id)
    if reply==None:
        print 'reply is none'
        result ={'code':1,'message':'reply is none','comment':''}
        return result
    if create_user_id==0:
        print 'create_user_id is null'
        result = {'code': 1, 'message': 'create_user_id is null','comment':''}
        return result
    floor = reply.floor_num+1
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    data = db_model_comment.insert(content,create_user_id,reply_id,community_id,post_id,to_user_id,parent_id,floor,create_time)
    db_model_reply.update_floor_num(reply_id, floor)
    db_model_message.insert_comment_reply(data.id)
    data = db_model_comment.to_json(data)
    result = {'code': 0, 'message': 'success','comment':data}
    return result

def delete_by_id(request):
    #delete
    comment_id = request.args.get('comment_id', default_comment_id)
    print 'do delete comment'
    db_model_comment.delete(comment_id)