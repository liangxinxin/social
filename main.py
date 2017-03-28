# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask import jsonify
from flask import redirect, url_for

from modules import mod_comment
from modules import mod_community
from modules import mod_image
from modules import mod_login
from modules import mod_logout
from modules import mod_message
from modules import mod_mobile
from modules import mod_post
from modules import mod_private_message
from modules import mod_reply
from modules import mod_user
from modules import mod_user_community
from modules import mod_verify
from modules import time_format

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
    page_no, page_size, post_list = mod_post.select_good_post(request)
    total_size = mod_post.select_goodpost_all()
    post_list_new=[]
    for post_new in post_list:
        post_new.last_update_time=time_format.timestampFormat(post_new.last_update_time)
        post_list_new.append(post_new)
    messages_unread = mod_user.get_unread_message_from_session()
    count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)
    if messages_unread != None:
        messages_unread_num=len(messages_unread)
        private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)
        return render_template('good_post_list.html', post_list=post_list_new, num=len(post_list), no=page_no, size=page_size, \
                               private_unread_count=private_unread_count,\
                               count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu, count_do_good=count_do_good,\
            totalsize=total_size,messages_unread=messages_unread,messages_unread_num=messages_unread_num,flag=1)

    return redirect('/index')



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
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)
    if communities != None:
        print 'default coumunity list. data list len:', len(communities)
        messages_unread=mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('index.html', target_list=communities, num=len(communities), no=page_no, size=page_size, \
                               private_unread_count=private_unread_count,count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
                               totalsize=total_size,messages_unread=messages_unread,messages_unread_num=messages_unread_num)
    else:
        messages_unread = mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('index.html', target_list=communities, num=0, no=page_no, size=0, totalsize=0, \
                               count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,
                               count_do_good=count_do_good, \
                               messages_unread=messages_unread,messages_unread_num=messages_unread_num)


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
    messages_unread=mod_user.get_unread_message_from_session()
    messages_unread_num = 0
    count_comment = 0
    count_reply = 0
    count_guanzhu = 0
    count_do_good = 0
    if messages_unread != None:
        messages_unread_num=len(messages_unread)
        private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)
    return render_template('community_index.html',count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
                           private_unread_count=private_unread_count,messages_unread=messages_unread,messages_unread_num=messages_unread_num)


@app.route('/community_search', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community_search():
    model, search_name = mod_community.service(request)
    messages_unread_num = 0
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)
    if model != None:
        print 'data list len:', len(model.items), " search_name:", search_name
        messages_unread=mod_user.get_unread_message_from_session()

        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('community_search_result.html', paginate=model, object_list=model.items,\
            num=len(model.items), name=search_name,\
            count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
            private_unread_count=private_unread_count,\
            messages_unread=messages_unread,messages_unread_num=messages_unread_num)
    else:
        messages_unread=mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('community_search_result.html', paginate=model, object_list=None, num=0,\
            name=search_name,\
            messages_unread=messages_unread,messages_unread_num=messages_unread_num)


@app.route('/community_new', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community_new():
    messages_unread=mod_user.get_unread_message_from_session()
    messages_unread_num = 0
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)

    if messages_unread != None:
        messages_unread_num=len(messages_unread)
    return render_template('community_new.html', name=request.args.get('name'), \
                           private_unread_count=private_unread_count,\
                           count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
        messages_unread=messages_unread,messages_unread_num=messages_unread_num)


@app.route('/community_create', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community_create():
    model, community, has_join = mod_community.service(request)
    messages_unread_num = 0
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)
    #  print model,community_id
    if model != None and len(model.items) > 0:
        messages_unread=mod_user.get_unread_message_from_session()
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('community.html', paginate=model, object_list=model.items, community=community, \
                               has_join=has_join,private_unread_count=private_unread_count, \
                               count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
                               messages_unread=messages_unread,messages_unread_num=messages_unread_num)
    else:
        messages_unread=mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('community.html', community=community, has_join=has_join, \
                               messages_unread=messages_unread,messages_unread_num=messages_unread_num)


@app.route('/community', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community():
    model, user_list, community, has_join, page_no, real_num, num_perpage = mod_post.service(request)
    print 'has_join:', has_join
    post_num = len(model.items)
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)

    if model != None and community != None:
        messages_unread=mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('community.html', paginate=model, post_num=post_num, object_list=model.items,\
            user_list=user_list, community=community, has_join=has_join, page_no=page_no,\
            real_num=real_num,num_perpage=num_perpage,\
            count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
            private_unread_count=private_unread_count,\
            messages_unread=messages_unread,messages_unread_num=messages_unread_num)
    else:
        #    return render_template('community.html', community=community)
        messages_unread=mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('community_index.html',\
            messages_unread=messages_unread,messages_unread_num=messages_unread_num)

@app.route('/community_info', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def get_community_info():
    community= mod_community.get_community_info(request)
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)

    if community != None:
        messages_unread=mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('community_info.html', community=community,private_unread_count=private_unread_count,\
        count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
            messages_unread=messages_unread,messages_unread_num=messages_unread_num)
    else:
        #    return render_template('community.html', community=community)
        messages_unread=mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
        return render_template('community_index.html',\
           count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
            messages_unread=messages_unread,messages_unread_num=messages_unread_num)


@app.route('/post_publish', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def post_publish():
    model, user_list, community, has_join = mod_post.service(request)
    post_num = len(model.items)
    print model
    messages_unread=mod_user.get_unread_message_from_session()
    messages_unread_num = 0
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)

    if messages_unread != None:
        messages_unread_num=len(messages_unread)
    return render_template('community.html', paginate=model, post_num=post_num,\
        object_list=model.items,user_list=user_list, community=community, has_join=has_join, \
        private_unread_count=private_unread_count,count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
        messages_unread=messages_unread,messages_unread_num=messages_unread_num)


@app.route('/post', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def post():
    post_data, post_user, reply_data, reply_user_list, community, page_no, real_num, num_perpage, like_stats, liked_by_user,\
        best_reply,best_reply_user = mod_post.post_info(request)
    reply_num = len(reply_data.items)
    total_page = reply_data.pages

    #  print model
    if reply_data == None:
        messages_unread=mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
            private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)

        return render_template('post.html', post_data=post_data, post_user=post_user, community=community, \
                               messages_unread=messages_unread,messages_unread_num=messages_unread_num, \
                               count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu, count_do_good=count_do_good)
    else:
        messages_unread=mod_user.get_unread_message_from_session()
        messages_unread_num = 0
        if messages_unread != None:
            messages_unread_num=len(messages_unread)
            private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)

        return render_template('post.html', post_data=post_data, post_user=post_user, reply_num=reply_num, \
                               reply_list=reply_data.items,total_page=total_page,private_unread_count=private_unread_count, \
                               reply_user_list=reply_user_list, community=community, page_no=page_no, real_num=real_num, \
                               num_perpage=num_perpage, like_stats=like_stats, liked_by_user=liked_by_user, \
                               messages_unread=messages_unread,messages_unread_num=messages_unread_num, \
                               count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,\
                               count_do_good=count_do_good,best_reply=best_reply,best_reply_user=best_reply_user)


@app.route('/reply_publish', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def reply_publish():
    login_flag = mod_user.check_login()
    post_data, post_user, reply_data, reply_user_list, community, page_no, real_num, num_perpage, like_stats, liked_by_user=mod_reply.service(request)
    reply_num = len(reply_data.items)
    total_page = reply_data.pages
    messages_unread=mod_user.get_unread_message_from_session()
    messages_unread_num = 0
    count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)
    if messages_unread != None:
        messages_unread_num=len(messages_unread)

    # upd by lxx,redirect to post by pageno;  post is method name
    return redirect(url_for('post',post_id=post_data.id,page_no=total_page,community_id=post_data.community_id))

    # return render_template('post.html', post_data=post_data, post_user=post_user, reply_num=reply_num,\
    #     reply_list=reply_data.items, total_page=total_page, \
    #     reply_user_list=reply_user_list, community=community, page_no=page_no, real_num=real_num,\
    #     count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
    #     num_perpage=num_perpage, like_stats=like_stats, liked_by_user=liked_by_user,\
    #     messages_unread=messages_unread,messages_unread_num=messages_unread_num)


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
    result = mod_logout.service(request)
    return jsonify(succ=result['succ'],code=result['code'],message=result['message'])

@app.route('/user_create', methods=['GET', 'POST'])
def user_create():
    next_url = request.args.get('next_url')
    mobile = request.args.get('mobile')
    print next_url
    return render_template('user_create.html', next_url=next_url, mobile=mobile)

@app.route('/user_create_step_2', methods=['GET', 'POST'])
def user_create_step_2():
    return render_template('user_create_step2.html')

@app.route('/do_user_create', methods=['GET', 'POST'])
def do_user_create():
    model = mod_user.service(request)
    return jsonify(result='succ')


@app.route('/user_community', methods=['GET', 'POST'])
def user_community():
    community_user_num = mod_user_community.service(request)
    return jsonify(user_num=community_user_num)

@app.route('/message_reply_post', methods=['GET', 'POST'])
def message_reply_post():
    post_data,post_user,reply_data,reply_user = mod_message.service(request)
    messages_unread=mod_user.get_unread_message_from_session()
    messages_unread_num = 0
    if messages_unread != None:
        messages_unread_num=len(messages_unread)
    return render_template('message_reply_post.html',post_data=post_data,post_user=post_user,\
        reply_data=reply_data,reply_user=reply_user,\
        messages_unread=messages_unread,messages_unread_num=messages_unread_num)

@app.route('/message_praise_reply', methods=['GET', 'POST'])
def message_praise_reply():
    reply_data,reply_user,reply_like_count = mod_message.service(request)
    messages_unread=mod_user.get_unread_message_from_session()
    messages_unread_num = 0
    if messages_unread != None:
        messages_unread_num=len(messages_unread)
    return render_template('message_praise_reply.html',\
        reply_data=reply_data,reply_user=reply_user,reply_like_count=reply_like_count,\
        messages_unread=messages_unread,messages_unread_num=messages_unread_num)

@app.route('/read_message', methods=['GET', 'POST'])
def read_message():
    unread_message_num = mod_message.service(request)
    return jsonify(unread_message_num=unread_message_num)

# user_info start
@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    user_info = mod_user.service(request)
    #friends, page_no, num_perpage, friends_total = mod_user.good_friends(request)
    messages_unread = mod_user.get_unread_message_from_session()
    messages_unread_num = 0
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)
    if messages_unread != None:
        messages_unread_num = len(messages_unread)
    return render_template('user_info.html', user_info=user_info,\
                           count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,\
                           count_do_good=count_do_good,private_unread_count=private_unread_count, \
                           messages_unread=messages_unread, messages_unread_num=messages_unread_num)

@app.route('/user_info_post', methods=['GET'])
def user_info_post():
    print 'user_info_post start'
    post_list, page_no, num_perpage, total= mod_user.get_user_post(request)
    return jsonify(post_list=post_list,no=page_no,size=num_perpage,totalsize=total)



@app.route('/get_post_reply', methods=['GET'])
def user_info_get_reply():
    print 'user_info_friends start'
    reply_list, page_no, num_perpage,total= mod_reply.get_reply_by_post(request)
    return jsonify(reply_list=reply_list,no=page_no, size=num_perpage,totalsize=total)


@app.route('/user_info_publish_reply', methods=['POST'])
def user_info_publish_reply():
    print 'user_info_pubreply start'
    reply, floor_num= mod_reply.publish_reply_in_UserInfo(request)
    return jsonify(reply=reply,floor_num=floor_num)

@app.route('/good_friends',methods=['GET','post'])
# @interceptor(login_required=True)
def get_good_friends():
    print 'get_good_friends'
    friends, page_no, num_perpage, friends_total = mod_user.good_friends(request)
    return jsonify(friends=friends,no=page_no,size=num_perpage,totalsize=friends_total)
# user_info end

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    print "now begin verify"
    result = mod_verify.service(request)
    print result['succ']
    if result['succ'] == '0':
      print "verify pass! now begin insert db"
      result,user_info = mod_user.service(request)
    print "now begin return regist result"
    return jsonify(succ=result['succ'],code=result['code'],message=result['message'])
    #return json_result
   # print jsonify(succ='0',code='1',message='hehe')
   # print jsonify(succ=result['succ'],code=result['code'],message=result['message'])
   # return jsonify(succ='0')
   # return jsonify(succ=result['succ'],code=result['code'],message=result['message'])

@app.route('/modify_user', methods=['GET', 'POST'])
def modify_user():
    print "enter url modify_user"
    result = mod_user.service(request)
    print 'modify user result:',result
    return jsonify(succ=result['succ'],code=result['code'],message=result['message'])

@app.route('/check_mobile', methods=['GET', 'POST'])
def check_mobile():
    result = mod_mobile.service(request)
    print 'mobile check result:',result
    return jsonify(succ=result['succ'],code=result['code'],message=result['message'])

@app.route('/check_mobile_exist', methods=['GET', 'POST'])
def check_mobile_exist():
    result = mod_mobile.service(request)
    print 'mobile check result:',result
    return jsonify(succ=result['succ'],code=result['code'],message=result['message'])

@app.route('/check_user_name', methods=['GET', 'POST'])
def check_user_name():
    result = mod_user.service(request)
    return jsonify(succ=result['succ'],code=result['code'],message=result['message'])

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    return render_template('find_password.html')

@app.route('/index', methods=['GET', 'POST'])
def good_post_list():
    page_no, page_size, post_list = mod_post.select_good_post(request)
    total_size = mod_post.select_goodpost_all()
    post_list_new=[]
    for post_new in post_list:
        post_new.last_update_time=time_format.timestampFormat(post_new.last_update_time)
        post_list_new.append(post_new)
    messages_unread = mod_user.get_unread_message_from_session()
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)
    messages_unread_num=0
    if messages_unread != None:
        messages_unread_num=len(messages_unread)
    return render_template('good_post_list.html', post_list=post_list_new, num=len(post_list), no=page_no, size=page_size, \
                           private_unread_count=private_unread_count, count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,count_do_good=count_do_good, \
                           totalsize=total_size,messages_unread=messages_unread,messages_unread_num=messages_unread_num,flag=1)

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


@app.route('/get_comment',methods=['get'])
# @interceptor(login_required=True)
def get_comment():
    print 'get_comment'
    paginate = mod_comment.query_by_reply_id(request)
    return jsonify(result=paginate.items,has_next=paginate.has_next)

@app.route('/publish_comment',methods=['post'])
# @interceptor(login_required=True)
def publish_comment():
    print 'publish_comment'
    result = mod_comment.service(request)
    print 'publish_comment result:code '+str(result.get('code'))+' message: '+result.get('message')
    return jsonify(result)

@app.route('/message',methods=['GET', 'POST'])
# @interceptor(login_required=True)
def get_message():
    print 'get_message'
    login_flag = mod_user.check_login()
    if not login_flag:
        print 'user not login'
        return redirect('/index')
    messages_unread = mod_user.get_unread_message_from_session()
    messages_unread_num=0
    if messages_unread !=None:
        messages_unread_num = len(messages_unread)
    read_list, unread_list, total, page_no, num_perpage,message_type = mod_message.service(request)
    private_unread_count,count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(request)

    return render_template('message.html',
                           messages_unread_num=messages_unread_num,
                           count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu,
                           count_do_good=count_do_good,private_unread_count=private_unread_count, \
                           message_type=message_type,read_list=read_list,unread_list=unread_list,unread_num=len(unread_list),read_num=len(read_list),
                           totalsize=total,size=num_perpage,no=page_no)

@app.route('/private_message',methods=['GET', 'POST'])
# @interceptor(login_required=True)
def private_message():
   login_flag = mod_user.check_login()
   if not login_flag:
       return redirect('/index')
   user_list,unread_count_list,user_num = mod_private_message.select_recent_user(request)

   return render_template('private_message.html',user_list=user_list,unread_count_list=unread_count_list,user_num=user_num)


@app.route('/save_message',methods=['GET', 'POST'])
# @interceptor(login_required=True)
def saveMessage():
   data = mod_private_message.save_private_message(request)
   return jsonify(result=data)

@app.route('/get_new_message',methods=['GET', 'POST'])
# @interceptor(login_required=True)
def newMessage():
   data = mod_private_message.select_new_message(request)
   return jsonify(result=data)

# to do  点击人后加载此用户聊天信息
@app.route('/get_user_message',methods=['GET', 'POST'])
# @interceptor(login_required=True)
def getUserMessage():
    mess_list = mod_private_message.select_mess_by_user(request)
    return jsonify(result=mess_list)

'''  MAIN ENTRY  '''
if __name__ == '__main__':
    app.debug = True
    ##项目启动 只查询一次默认图片数据
    user_data, comm_data = mod_image.select_default_image()
    default_user_data = user_data
    default_community_data = comm_data
    app.run(host="0.0.0.0", port=6100, processes=6)
