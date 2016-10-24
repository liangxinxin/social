from flask import session
from db_interface import db_model_user

def service(request):
	model = {}
	name = request.form['name']
	password = request.form['password']
	user = db_model_user.select_by_name_and_password(name=name,password=password)
	if user is not None:
		session['userinfo'] = {'name':user.name, 'id':user.id}
		model['result'] = True
	else:
		model['result'] = False
	return model
