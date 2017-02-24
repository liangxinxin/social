from flask import session
from db_interface import db_model_message
from db_interface import db_model_user
from db_interface import db_model_post
from db_interface import db_model_reply
from db_interface import db_model_reply_like_stat

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
    return 0
    

