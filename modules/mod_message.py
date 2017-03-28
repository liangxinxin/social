from flask import session
from db_interface import db_model_message
from db_interface import db_model_user
from db_interface import db_model_post
from db_interface import db_model_reply
from db_interface import db_model_reply_like_stat
from db_interface import db_model_comment
from db_interface import db_model_private_message
default_page_no=1
default_num_perpage=10


def service(request):
  print "enter do db_model_message  service"
  if request.method == 'POST':
    message_id=request.form.get("message_id")
    print " read message ",message_id
    if message_id != None:
      # change message status
      db_model_message.update_has_read(message_id,1)
      # get user unread message num and return
      info = db_model_message.select_by_id(message_id)
      user_to_id = info.user_to_id
      user_info = db_model_user.select_by_id(user_to_id)
      return len(user_info.messages.filter_by(has_read=False).all())
      print "use now have unread message num:",len(user_info.messages.filter_by(has_read=False).all())
    else:
      return 0
  elif request.method == 'GET':
    query_type=request.args.get('type')
    if query_type == 'message_reply_post':
      user_from_id = int(request.args.get('user_from_id'))
      user_to_id = int(request.args.get('user_to_id'))
      post_id = int(request.args.get('post_id'))  
      reply_id = int(request.args.get('reply_id'))
      post_data = db_model_post.select_by_id(post_id)
      post_user = db_model_user.select_by_id(user_to_id)
      reply_data = db_model_reply.select_by_id(reply_id)
      reply_user = db_model_user.select_by_id(user_from_id)
      return post_data,post_user,reply_data,reply_user
    elif query_type == 'message_praise_reply':
      user_from_id = int(request.args.get('user_from_id'))
      user_to_id = int(request.args.get('user_to_id'))
      reply_id = int(request.args.get('reply_id'))
      reply_data = db_model_reply.select_by_id(reply_id)
      reply_user = db_model_user.select_by_id(user_to_id)
      reply_like_count = db_model_reply_like_stat.get_reply_like_count(reply_id)
      return reply_data,reply_user,reply_like_count
    elif query_type=='message_all':
      return select_comment_message(request)
    return 0



def  select_comment_message(request):
  if session.get('userinfo'):
    to_userid = session.get('userinfo')['id']
    message_type = int(request.args.get('message_type')) # 1.guanzhu 2.zan 3.pinglun 4.huifu
    page_no = int(request.args.get("no", default_page_no))
    num_perpage = int(request.args.get("size", 2))
    read_list, unread_list= db_model_message.select_message_by_to_user(message_type, to_userid, page_no, num_perpage)
    total = read_list.total
    if message_type==4:
      for message in read_list.items:
        comment = message.comment
        if comment.parent_id != None:
          comment.parent  = db_model_comment.select_by_id(comment.parent_id)
          message.comment = comment
      unread_list_new = []
      for message in unread_list:
        db_model_message.update_has_read(message.id, True)
        comment = message.comment
        if comment.parent_id != None:
          comment.parent  = db_model_comment.select_by_id(comment.parent_id)
          message.comment = comment

    else:
      for message in unread_list:
        db_model_message.update_has_read(message.id, True)

    return read_list.items,unread_list,total,page_no,num_perpage,message_type



def select_unread_num_by_type(request):
  un_read = False
  if session.get('userinfo'):
    userid = session.get('userinfo')['id']
    private_unread_count = db_model_private_message.select_all_unread(userid)
    count_comment, count_reply, count_guanzhu, count_do_good = db_model_message.select_num_unread_by_type(un_read,userid)
    return private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good

  return 0,0,0,0,0

