from flask import session
from db_interface import db_model_message
from db_interface import db_model_user

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
  else:
    return 0
    

