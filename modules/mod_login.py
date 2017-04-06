import time
import time_format
from flask import session
from db_interface import db_model_user
from db_interface import db_model_action
from db_interface import db_model_action_type

def service(request):
	model = {}
	name = request.form['name']
	password = request.form['password']
	next_url=request.args.get('next_url')
        print "login:",name,password
	user1 = db_model_user.select_by_name_and_password(name=name,password=password)
	user2 = db_model_user.select_by_mobile_and_password(mobile=name,password=password)
	if user1 is not None :
		session['userinfo'] = {'name':user1.name, 'id':user1.id}
		model['result'] = True
                ISOTIMEFORMAT = '%Y-%m-%d %X'
                create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
                db_model_action.insert(user_id=user1.id,\
                    action_type_id=db_model_action_type.get_type_id('login'),action_detail_info='',\
                    create_time=create_time)
	elif user2 is not None:
		session['userinfo'] = {'name':user2.name, 'id':user2.id}
		model['result'] = True
                create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
                db_model_action.insert(user_id=user1.id,\
                    action_type_id=db_model_action_type.get_type_id('login'),action_detail_info='',\
                    create_time=create_time)
	else:
		model['result'] = False
	return model,next_url
