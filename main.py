# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask import jsonify
from flask import redirect, url_for

from modules import mod_community
from modules import mod_login
from modules import mod_logout
from modules import mod_post
from modules import mod_reply
from modules import mod_user
from modules import mod_user_community
from modules import time_format
from modules import mod_image

from modules.db_interface import db_model_user_relation

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
# app.secret_key = "super secret key"
# app.config['SECRET_KEY'] = 'super secret key'
app.config.from_object('config')

default_user_data=[]
default_community_data =[]


@app.route('/')
# @interceptor(login_required=True)
def default():
    return redirect(url_for('index'))


# @app.route('/index')
# # @interceptor(login_required=False)
# def index():
#     page_size = 20
#     communities = mod_community.get_default_communities(1, page_size)
#     total_size = mod_community.get_hot_communities_total_num()
#     if communities != None:
#         print 'default coumunity list. data list len:', len(communities)
#         return render_template('index.html', target_list=communities, num=len(communities), no=1, size=page_size,
#                                totalsize=total_size)
#     else:
#         return render_template('index.html', target_list=communities, num=0, no=1, size=0, totalsize=0)


@app.route('/indexpage')
# @interceptor(login_required=False)
def indexpage():
    page_no = int(request.args.get('no'))
    page_size = int(request.args.get('size'))
    total_size = mod_community.get_hot_communities_total_num()
    print "pageno:", page_no, "pagesize: ", page_size
    communities = mod_community.get_default_communities(page_no, page_size)
    if communities != None:
        print 'default coumunity list. data list len:', len(communities)
        return render_template('index.html', target_list=communities, num=len(communities), no=page_no, size=page_size,\
                               totalsize=total_size,messages_unread=mod_user.get_unread_message_from_session())
    else:
        return render_template('index.html', target_list=communities, num=0, no=page_no, size=0, totalsize=0,\
            messages_unread=mod_user.get_unread_message_from_session())


@app.route('/error', methods=['GET', 'POST'])
# @interceptor(login_required=False)
def error():
    msg = request.args.get('msg')
    return render_template('error.html', msg=msg)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', msg=e)


'''  BUSSINESS FUNCTIONS BEGIN  '''


@app.route('/community_index', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community_index():
    return render_template('community_index.html')


@app.route('/community_search', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community_search():
    model, search_name = mod_community.service(request)
    if model != None:
        print 'data list len:', len(model.items), " search_name:", search_name
        return render_template('community_search_result.html', paginate=model, object_list=model.items,
                               num=len(model.items), name=search_name)
    else:
        return render_template('community_search_result.html', paginate=model, object_list=None, num=0,
                               name=search_name)


@app.route('/community_new', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community_new():
    return render_template('community_new.html', name=request.args.get('name'))


@app.route('/community_create', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community_create():
    model, community, has_join = mod_community.service(request)
    #  print model,community_id
    if model != None and len(model.items) > 0:
        return render_template('community.html', paginate=model, object_list=model.items, community=community,
                               has_join=has_join)
    else:
        return render_template('community.html', community=community, has_join=has_join)


@app.route('/community', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community():
    model, user_list, community, has_join, page_no, real_num, num_perpage = mod_post.service(request)
    print 'has_join:', has_join
    post_num = len(model.items)
    if model != None and community != None:
        return render_template('community.html', paginate=model, post_num=post_num, object_list=model.items, \
                               user_list=user_list, community=community, has_join=has_join, page_no=page_no,
                               real_num=real_num, \
                               num_perpage=num_perpage)
    else:
        #    return render_template('community.html', community=community)
        return render_template('community_index.html')

@app.route('/community_info', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def get_community_info():
    community= mod_community.get_community_info(request)
    if community != None:
        return render_template('community_info.html', community=community)
    else:
        #    return render_template('community.html', community=community)
        return render_template('community_index.html')


@app.route('/post_publish', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def post_publish():
    model, user_list, community, has_join = mod_post.service(request)
    post_num = len(model.items)
    print model
    return render_template('community.html', paginate=model, post_num=post_num, object_list=model.items,
                           user_list=user_list, community=community, has_join=has_join)


@app.route('/post', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def post():
    post_data, post_user, reply_data, reply_user_list, community, page_no, real_num, num_perpage, like_stats, liked_by_user = mod_post.post_info(
        request)
    reply_num = len(reply_data.items)
    #  print model
    if reply_data == None:
        return render_template('post.html', post_data=post_data, post_user=post_user, community=community)
    else:
        return render_template('post.html', post_data=post_data, post_user=post_user, reply_num=reply_num,
                               reply_list=reply_data.items, \
                               reply_user_list=reply_user_list, community=community, page_no=page_no, real_num=real_num,
                               num_perpage=num_perpage, like_stats=like_stats, liked_by_user=liked_by_user)


@app.route('/reply_publish', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def reply_publish():
    post_data, post_user, reply_data, reply_user_list, community, page_no, real_num, num_perpage, like_stats, liked_by_user = mod_reply.service(
        request)
    reply_num = len(reply_data.items)
    return render_template('post.html', post_data=post_data, post_user=post_user, reply_num=reply_num,
                           reply_list=reply_data.items, \
                           reply_user_list=reply_user_list, community=community, page_no=page_no, real_num=real_num,
                           num_perpage=num_perpage, like_stats=like_stats, liked_by_user=liked_by_user)


@app.route('/reply_like_status_change', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def reply_like():
    mod_reply.reply_like_changed(request)
    return jsonify(res="status-changed")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if method is get, then show login page only.if post, then deal login request
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        model, next_url = mod_login.service(request)
        if model['result'] == True:
            return redirect(next_url)
        else:
            return render_template('login.html', msg='用户名或密码错误！')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    model, next_url = mod_logout.service(request)
    return redirect(next_url)


@app.route('/user_create', methods=['GET', 'POST'])
def user_create():
    next_url = request.args.get('next_url')
    print next_url
    return render_template('user_create.html', next_url=next_url)


@app.route('/do_user_create', methods=['GET', 'POST'])
def do_user_create():
    model = mod_user.service(request)
    return jsonify(result='succ')


@app.route('/user_community', methods=['GET', 'POST'])
def user_community():
    community_user_num = mod_user_community.service(request)
    return jsonify(user_num=community_user_num)


@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    user_info = mod_user.service(request)
    return render_template('user_info.html', user_info=user_info)


@app.route('/index', methods=['GET', 'POST'])
def good_post_list():
    page_no, page_size, post_list = mod_post.select_good_post(request)
    total_size = mod_post.select_goodpost_all()
    post_list_new=[]
    for post_new in post_list:
        post_new.last_update_time=time_format.timestampFormat(post_new.last_update_time)
        post_list_new.append(post_new)
    print "message----",mod_user.get_unread_message_from_session()
    return render_template('good_post_list.html', post_list=post_list_new, num=len(post_list), no=page_no, size=page_size,\
        totalsize=total_size,messages_unread=mod_user.get_unread_message_from_session(),flag=1)

@app.route('/add_relation',methods=['POST'])
# @interceptor(login_required=True)
def add_relation():
    mod_user.add_relation(request)
    return jsonify(result='succ')

@app.route('/cancel_relation',methods=['POST'])
# @interceptor(login_required=True)
def cancel_relation():
    mod_user.update_relation(request)
    return jsonify(result='succ')

@app.route('/select_relation',methods=['POST'])
# @interceptor(login_required=True)
def select_relation():
    is_relation = mod_user.select_relation_user_id(request)
    return jsonify(is_relation=is_relation)

@app.route('/upload_head_image',methods=['POST'])
# @interceptor(login_required=True)
def upload_head_image():
    print 'upload_head_image'
    result = mod_image.service(request)
    if result.get('code') == 0:
        return jsonify(code=0, result='succ')
    else:
        return jsonify(code=1, result='fail')

@app.route('/get_default_image',methods=['get'])
# @interceptor(login_required=True)
def get_default_image():
    type = request.args.get("type")
    print type+':get_default_image'
    if type == "user":
        return jsonify(result=default_user_data)
    else:
        return jsonify(result=default_community_data)



'''  MAIN ENTRY  '''
if __name__ == '__main__':
    app.debug = True
    ##项目启动 只查询一次默认图片数据
    user_data, comm_data = mod_image.select_default_image()
    default_user_data = user_data
    default_community_data = comm_data
    app.run(host="0.0.0.0", port=6100, processes=6)
