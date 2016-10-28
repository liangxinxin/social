from flask import Flask, request, render_template 
from flask import redirect, url_for
from flask import jsonify 

import os
import os.path

from modules import mod_community
from modules import mod_login
from modules import mod_logout
from modules import mod_post
from modules import mod_reply
from modules import mod_user
from modules import mod_user_community

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
#app.secret_key = "super secret key"
#app.config['SECRET_KEY'] = 'super secret key'
app.config.from_object('config')

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
  model,community,has_join = mod_community.service(request)
#  print model,community_id
  if model != None and len(model.items) > 0:
    return render_template('community.html', paginate=model,object_list=model.items,community=community,has_join=has_join)
  else:
    return render_template('community.html',community=community,has_join=has_join)

@app.route('/community', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def community():
  model,user_list,community,has_join = mod_post.service(request)
  print 'has_join:',has_join
  post_num=len(model.items) 
  if model != None and community!=None:
    return render_template('community.html', paginate=model,post_num=post_num,object_list=model.items,user_list=user_list,community=community,has_join=has_join)
  else:
#    return render_template('community.html', community=community)
    return render_template('community_index.html')

@app.route('/post_publish', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def post_publish():
  model,user_list,community,has_join = mod_post.service(request)
  post_num = len(model.items)
  print model
  return render_template('community.html', paginate=model,post_num=post_num,object_list=model.items,user_list=user_list,community=community,has_join=has_join)

@app.route('/post', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def post():
  post_data,post_user,reply_data,reply_user_list,community = mod_post.post_info(request)
  reply_num=len(reply_data.items)
#  print model
  if reply_data == None:
    return render_template('post.html',post_data=post_data,post_user=post_user,community=community)
  else:
    return render_template('post.html',post_data=post_data,post_user=post_user,reply_num=reply_num,reply_list=reply_data.items,reply_user_list=reply_user_list,community=community)

@app.route('/reply_publish', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def reply_publish():
  post_data,post_user,reply_data,reply_user_list,community = mod_reply.service(request)
  reply_num=len(reply_data.items)
  return render_template('post.html',post_data=post_data,post_user=post_user,reply_num=reply_num,reply_list=reply_data.items,reply_user_list=reply_user_list,community=community)

@app.route('/login',methods=['GET','POST'])
def login():
  #if method is get, then show login page only.if post, then deal login request
  if request.method == 'GET':
    return render_template('login.html')
  elif request.method == 'POST':
    model,next_url = mod_login.service(request)
    if model['result'] == True:
      return redirect(next_url)
    else:
      return render_template('error.html',msg='login error')

@app.route('/logout',methods=['GET','POST'])
def logout():
  model,next_url=mod_logout.service(request)
  return redirect(next_url)

@app.route('/user_create',methods=['GET','POST'])
def user_create():
  next_url = request.args.get('next_url')
  print next_url
  return render_template('user_create.html',next_url=next_url)

@app.route('/do_user_create',methods=['GET','POST'])
def do_user_create():
  model=mod_user.service(request)
  return jsonify(result='succ') 

@app.route('/user_community',methods=['GET','POST'])
def user_community():
  community_user_num=mod_user_community.service(request)
  return jsonify(user_num=community_user_num) 

@app.route('/user_info',methods=['GET','POST'])
def user_info():
  user_info=mod_user.service(request)
  return render_template('user_info.html',user_info=user_info)

'''  MAIN ENTRY  '''
if __name__ == '__main__':
  app.debug = True
  app.run(host="127.0.0.1",port=6100,processes=6)
