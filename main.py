from flask import Flask, request, render_template 
from flask import redirect, url_for

import os
import os.path

from modules import mod_community
from modules import mod_login
from modules import mod_logout
from modules import mod_post
from modules import mod_reply

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
#app.secret_key = "super secret key"
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/')
#@interceptor(login_required=True)
def default():
  model = [] 
  return render_template('index.html', model=model)

@app.route('/index')
#@interceptor(login_required=False)
def index():
  model = [] 
  return render_template('index.html', model=model)

@app.route('/error', methods=['GET', 'POST'])
#@interceptor(login_required=False)
def error():
  msg = request.args.get('msg')
  return render_template('error.html',msg=msg)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html',msg=e)


'''  BUSSINESS FUNCTIONS BEGIN  '''



@app.route('/community_index', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def community_index():
  return render_template('community_index.html')

@app.route('/community_search', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def community_search():
  model,search_name = mod_community.service(request)
  if model != None:
    print 'data list len:',len(model.items)
    return render_template('community_search_result.html',paginate=model,object_list=model.items,num=len(model.items),name=search_name)
  else:
    return render_template('community_search_result.html',paginate=model,object_list=None,num=0,name=search_name)

@app.route('/community_new', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def community_new():
  return render_template('community_new.html', name=request.args.get('name'))

@app.route('/community_create', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def community_create():
  model,community_id = mod_community.service(request)
  print model,community_id
  if model != None and len(model.items) > 0:
    return render_template('community.html', paginate=model,object_list=model.items,community_id=community_id)
  else:
    return render_template('community.html',community_id=community_id)

@app.route('/community', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def community():
  model,community_id = mod_post.service(request)
  print community_id
  if model != None:
    return render_template('community.html', paginate=model,object_list=model.items,community_id=community_id)
  else:
    return render_template('community.html', community_id=community_id)

@app.route('/post_publish', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def post_publish():
  model,community_id = mod_post.service(request)
  print model
  return render_template('community.html', paginate=model,object_list=model.items,community_id=community_id)

@app.route('/post', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def post():
  post_data,reply_data = mod_post.post_info(request)
#  print model
  if reply_data != None:
    return render_template('post.html',post_data=post_data)
  else:
    return render_template('post.html',post_data=post_data,reply_list=reply_data.items)

@app.route('/reply_publish', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def reply_publish():
  post_data,reply_data = mod_reply.service(request)
  return render_template('post.html',post_data=post_data,reply_list=reply_data.items)

@app.route('/login',methods=['GET','POST'])
def login():
  #if method is get, then show login page only.if post, then deal login request
  if request.method == 'GET':
    return render_template('login.html')
  elif request.method == 'POST':
    model,recommend_content=mod_login.service(request)
    if model['result'] == True:
      return render_template('index.html', recommend_content=recommend_content)
    else:
      return render_template('error.html',msg='login error')
      #return render_template('index.html',model=model,recommend=recommend_content)

@app.route('/logout',methods=['GET','POST'])
def logout():
  model=mod_logout.service(request)
  return render_template('index.html')

'''  MAIN ENTRY  '''
if __name__ == '__main__':
  app.debug = True
  app.run(host="127.0.0.1",port=6100,processes=6)
