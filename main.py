# -*- coding: utf-8 -*-
import time

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

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
# app.secret_key = "super secret key"
# app.config['SECRET_KEY'] = 'super secret key'
app.config.from_object('config')

default_user_data = []
default_community_data = []


@app.route('/')
# @interceptor(login_required=True)
def default():
    return redirect('/index')


@app.route('/error', methods=['GET', 'POST'])
# @interceptor(login_required=False)
def error():
    msg = request.args.get('msg')
    return render_template('error.html', msg=msg)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', msg=e)


'''  BUSSINESS FUNCTIONS BEGIN  '''


@app.route('/find_match_community', methods=['GET'])
# @interceptor(login_required=True)
def find_match_community():
    comm_list = mod_community.find_match_community(request)
    return jsonify(comm_list=comm_list)


@app.route('/community_create', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community_create():
    result = mod_community.service(request)
    return jsonify(code=result['code'], community=result['data'])


@app.route('/community', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community():
    community, has_join, create_user = mod_community.service(request)
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    return render_template('community.html', has_join=has_join, community=community, create_user=create_user,
                           mess_dict=mess_dict, messages_unread_num=messages_unread_num)


@app.route('/get_community_post', methods=['GET'])
def get_community_post():
    print 'get_community_post'
    model, page_no, num_perpage = mod_post.service(request)
    total = model.total
    print 'get_community_post rersult total', total
    return jsonify(post_list=model.items, page_no=page_no, total=total)


@app.route('/get_commend_community', methods=['GET'])
def get_commend_community():
    page_no, num_page, commend_list = mod_community.select_hot_commend_community(request)
    print 'get_commend_community', 'total', len(commend_list)
    return jsonify(page_no=page_no, num_page=num_page, commend_list=commend_list)


@app.route('/update_community', methods=['POST'])
def update_community():
    result = mod_community.service(request)
    print 'update_community result', result['code'], result['message']
    return jsonify(result=result['code'])


@app.route('/post_publish', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def post_publish():
    model, user_list, community, has_join = mod_post.service(request)
    post_num = len(model.items)
    print model
    return redirect(url_for('community', id=community.id, type='query'))


@app.route('/post', methods=['GET'])
# @interceptor(login_required=True)
def post():
    post = mod_post.service(request)
    if post:
        has_join = mod_user_community.user_has_join_community(post.community_id)
        mess_dict = mod_message.select_unread_num_by_type()
        messages_unread_num = mod_user.get_unread_message_from_session()
        return render_template('post.html', post=post, has_join=has_join, messages_unread_num=messages_unread_num,
                               mess_dict=mess_dict)
    else:
        msg = '页面找不到了'
        redirect(url_for('error', msg=''))
    return render_template('error.html', msg=msg)


# show reply and best in post.html
@app.route('/get_reply', methods=['GET'])
def get_best_reply():
    reply_list, best_reply, like_user_dict, page_no, num_perpage, total_page, total = mod_reply.service(request)
    return jsonify(reply_list=reply_list, best_reply=best_reply, like_user_dict=like_user_dict,
                   page_no=page_no, num_perpage=num_perpage, total=total)


@app.route('/delete_post', methods=['POST'])
# @interceptor(login_required=True)
def delete_post():
    result = mod_post.delete_post(request)
    print 'delete commpelete result:', result['code'],result['message']
    return jsonify(result=result['code'])


@app.route('/find_match_post', methods=['GET'])
# @interceptor(login_required=True)
def find_match_post():
    post_list = mod_post.find_match_post(request)
    return jsonify(post_list=post_list)


@app.route('/reply_publish', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def reply_publish():
    reply, replycount, total_page = mod_reply.service(request)
    return jsonify(reply=reply, replycount=replycount, total_page=total_page)


@app.route('/update_reply', methods=['POST'])
# @interceptor(login_required=True)
def reply_update():
    print 'reply_update'
    result = mod_reply.update_reply(request)
    print 'reply_update result', result['code']
    return jsonify(result=result['code'])


@app.route('/delete_reply', methods=['POST'])
# @interceptor(login_required=True)
def delete_reply():
    result = mod_reply.service(request)
    return jsonify(code=result['code'],replycount = result['replycount'])


@app.route('/reply_like_status_change', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def reply_like():
    result = mod_reply.reply_like_changed(request)
    return jsonify(code=result['code'], like_num=result['like_num'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if method is get, then show login page only.if post, then deal login request
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        model, next_url = mod_login.service(request)
        if model['result']:
            return redirect(next_url)
        else:
            return render_template('login.html', msg='用户名或密码错误！')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    result = mod_logout.service(request)
    return jsonify(succ=result['succ'], code=result['code'], message=result['message'])


@app.route('/user_create', methods=['GET', 'POST'])
def user_create():
    next_url = request.args.get('next_url')
    mobile = request.args.get('mobile')
    print next_url
    return render_template('user_create.html', next_url=next_url, mobile=mobile)


@app.route('/user_create_step_2', methods=['GET', 'POST'])
def user_create_step_2():
    return render_template('user_create_step_2.html')


@app.route('/do_user_create', methods=['GET', 'POST'])
def do_user_create():
    model = mod_user.service(request)
    return jsonify(result='succ')


@app.route('/update_user', methods=['POST'])
def update_user():
    result = mod_user.update_user(request)
    return jsonify(result=result['code'])


@app.route('/user_community', methods=['GET', 'POST'])
def user_community():
    community_user_num = mod_user_community.service(request)
    return jsonify(user_num=community_user_num)


@app.route('/read_message', methods=['GET', 'POST'])
def read_message():
    unread_message_num = mod_message.service(request)
    return jsonify(unread_message_num=unread_message_num)


# # user_info start
# @app.route('/user_info', methods=['GET', 'POST'])
# def user_info():
#     user_info = mod_user.service(request)
#     messages_unread = mod_user.get_unread_message_from_session()
#     messages_unread_num = 0
#     private_unread_count, count_comment, count_reply, count_guanzhu, count_do_good = mod_message.select_unread_num_by_type(
#         request)
#     if messages_unread:
#         messages_unread_num = len(messages_unread)
#     return render_template('user_info.html', user_info=user_info, \
#                            count_comment=count_comment, count_reply=count_reply, count_guanzhu=count_guanzhu, \
#                            count_do_good=count_do_good, private_unread_count=private_unread_count, \
#                            messages_unread=messages_unread, messages_unread_num=messages_unread_num)


@app.route('/user_info_post', methods=['GET', 'POST'])
def user_info_post():
    print 'user_info_post start'
    post_list, page_no, num_perpage, total, view_user_info = mod_user.get_user_post(request)
    messages_unread_num = mod_user.get_unread_message_from_session()
    mess_dict = mod_message.select_unread_num_by_type()
    user_info_type = 'post'
    print 'user_info_type', user_info_type
    return render_template('user_info_post.html', mess_dict=mess_dict,messages_unread=messages_unread_num,
                           messages_unread_num=messages_unread_num,post_list=post_list, no=page_no,size=num_perpage,
                           total_size=total,view_user_info=view_user_info, user_info_type=user_info_type)


@app.route('/user_info_community_create', methods=['GET', 'POST'])
def user_info_community_create():
    print 'user_info_community_owned start'
    messages_unread_num = mod_user.get_unread_message_from_session()
    community_list, page_no, num_perpage, total, view_user_info = mod_user.community_create(request)
    mess_dict = mod_message.select_unread_num_by_type()
    user_info_type = 'community_create'
    return render_template('user_info_community_create.html', mess_dict=mess_dict, messages_unread=messages_unread_num,
                           messages_unread_num=messages_unread_num,community_list=community_list, no=page_no,
                           size=num_perpage, total_size=total,view_user_info=view_user_info,
                           user_info_type=user_info_type)


# into the followed html
@app.route('/user_info_community_join', methods=['GET'])
def user_info_community_join():
    view_user_info = mod_user.service(request)
    user_info_type = 'community_join'
    messages_unread_num = mod_user.get_unread_message_from_session()
    mess_dict = mod_message.select_unread_num_by_type()
    return render_template('user_community_followed.html', view_user_info=view_user_info, user_info_type=user_info_type,
                           mess_dict=mess_dict,messages_unread_num=messages_unread_num)


# load data:community the user join
@app.route('/community_joined', methods=['GET'])
def community_joined():
    community_list, page_no, num_perpage, total_count, total_pages = mod_user_community.service(request)
    return jsonify(community_list=community_list,no=page_no, size=num_perpage, totalCount=total_count, totalPages=total_pages)


@app.route('/user_info_friend', methods=['GET', 'POST'])
def user_info_friend():
    print 'user_info_friend start'
    friend_list, page_no, num_perpage, total, view_user_info = mod_user.good_friends(request)
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    user_info_type = 'friend'
    return render_template('user_info_friend.html',mess_dict=mess_dict, messages_unread_num=messages_unread_num,
                           friend_list=friend_list, no=page_no, size=num_perpage, total_size=total,
                           view_user_info=view_user_info, user_info_type=user_info_type)


@app.route('/community_owned', methods=['GET', 'post'])
# @interceptor(login_required=True)
def get_community_owned():
    print 'get_community_owned'
    communities, page_no, num_perpage, communities_total = mod_user.community_owned(request)
    return jsonify(communities=communities, no=page_no, size=num_perpage, totalsize=communities_total)



@app.route('/good_friends', methods=['GET', 'post'])
# @interceptor(login_required=True)
def get_good_friends():
    print 'get_good_friends'
    friends, page_no, num_perpage, friends_total = mod_user.good_friends(request)
    return jsonify(friends=friends, no=page_no, size=num_perpage, totalsize=friends_total)


# user_info end

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('register.html')
    print "now begin verify"
    result = mod_verify.service(request)
    print 'check smscode result code:',result['code'],'message,',result['message']
    if result['succ'] == '0':
        print "verify pass! now begin insert db"
        result, user_info = mod_user.service(request)
    print "now begin return regist result"
    return jsonify(succ=result['succ'], code=result['code'], message=result['message'])


@app.route('/modify_user', methods=['GET', 'POST'])
def modify_user():
    print "enter url modify_user"
    result = mod_user.service(request)
    print 'modify user result:', result
    return jsonify(succ=result['succ'], code=result['code'], message=result['message'])


@app.route('/check_mobile', methods=['GET', 'POST'])
def check_mobile():
    result = mod_mobile.service(request)
    print 'mobile check result:', result
    return jsonify(succ=result['succ'], code=result['code'], message=result['message'])


@app.route('/check_mobile_exist', methods=['GET', 'POST'])
def check_mobile_exist():
    result = mod_mobile.service(request)
    print 'mobile check result:', result
    return jsonify(succ=result['succ'], code=result['code'], message=result['message'])


@app.route('/check_user_name', methods=['GET', 'POST'])
def check_user_name():
    result = mod_user.service(request)
    return jsonify(succ=result['succ'], code=result['code'], message=result['message'])


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    return render_template('find_password.html')


@app.route('/index', methods=['GET'])
def index():
    count = mod_post.service(request)
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    return render_template('index.html', total=count, mess_dict=mess_dict, messages_unread_num=messages_unread_num)


@app.route('/get_hot_post', methods=['GET'])
def good_post_list():
    page_no, num_perpage, post_list, total = mod_post.service(request)
    return jsonify(page_no=page_no, num_perpage=num_perpage, post_list=post_list, total=total)


@app.route('/get_hot_community', methods=['GET'])
def get_hot_community():
    page_no, num_perpage, commend_list = mod_community.service(request)
    return jsonify(page_no=page_no, num_perpage=num_perpage, commend_list=commend_list)


@app.route('/add_relation', methods=['POST'])
# @interceptor(login_required=True)
def add_relation():
    mod_user.add_relation(request)
    return jsonify(result='succ')


@app.route('/cancel_relation', methods=['POST'])
# @interceptor(login_required=True)
def cancel_relation():
    mod_user.update_relation(request)
    return jsonify(result='succ')


@app.route('/select_relation', methods=['POST'])
# @interceptor(login_required=True)
def select_relation():
    is_relation = mod_user.select_relation_user_id(request)
    return jsonify(is_relation=is_relation)


@app.route('/upload_head_image', methods=['POST'])
# @interceptor(login_required=True)
def upload_head_image():
    print 'upload_head_image'
    result = mod_image.service(request)
    if result.get('code') == 0:
        return jsonify(code=0, result='succ', data=result['data'])
    else:
        return jsonify(code=1, result='fail', data='')


@app.route('/get_default_image', methods=['get'])
# @interceptor(login_required=True)
def get_default_image():
    type = request.args.get("type")
    if type == "user":
        return jsonify(result=default_user_data)
    else:
        return jsonify(result=default_community_data)

# more comment
@app.route('/get_comment', methods=['get'])
# @interceptor(login_required=True)
def get_comment():
    print 'get_comment'
    paginate = mod_comment.service(request)
    return jsonify(comment_list=paginate.items, has_next=paginate.has_next)


@app.route('/publish_comment', methods=['post'])
# @interceptor(login_required=True)
def publish_comment():
    print 'publish_comment'
    result = mod_comment.service(request)
    print 'publish_comment result:code ', result['code'], ' message: ', result['message']
    return jsonify(code=result['code'], comment=result['comment'])


@app.route('/delete_comment', methods=['post'])
# @interceptor(login_required=True)
def delete_comment():
    print 'delete_comment'
    result = mod_comment.service(request)
    print 'delete_comment result:code ', result.get('code')
    return jsonify(result=result['code'])


@app.route('/message', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def get_message():
    print 'get_message'
    login_flag = mod_user.check_login()
    if not login_flag:
        print 'user not login'
        return redirect('/index')
    messages_unread_num = mod_user.get_unread_message_from_session()
    read_list, unread_list, total, page_no, num_perpage, message_type = mod_message.service(request)
    mess_dict = mod_message.select_unread_num_by_type()
    view_user_info = mod_user.service(request)
    return render_template('message.html',messages_unread_num=messages_unread_num, view_user_info=view_user_info,
                           mess_dict=mess_dict, message_type=message_type, read_list=read_list, unread_list=unread_list,
                           unread_num=len(unread_list), read_num=len(read_list), total_size=total, size=num_perpage,
                           no=page_no)


@app.route('/private_message', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def private_message():
    to_user, user_list, unread_count_list, user_num = mod_private_message.select_recent_user(request)
    ISOTIMEFORMAT = '%Y-%m-%d'
    today = time.strftime(ISOTIMEFORMAT, time.localtime())
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    return render_template('private_message.html', today=today, to_user=to_user, user_list=user_list,
                           unread_count_list=unread_count_list, user_num=user_num, mess_dict=mess_dict,
                           messages_unread_num=messages_unread_num)


@app.route('/save_message', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def save_essage():
    data = mod_private_message.save_private_message(request)
    return jsonify(result=data)


@app.route('/get_new_message', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def new_essage():
    data = mod_private_message.service(request)
    return jsonify(result=data)


# to do  点击人后加载此用户聊天信息
@app.route('/get_history_message', methods=['GET'])
# @interceptor(login_required=True)
def get_history_message():
    mess_list = mod_private_message.service(request)
    return jsonify(result=mess_list)


'''  MAIN ENTRY  '''
if __name__ == '__main__':
    app.debug = True
    ##项目启动 只查询一次默认图片数据
    user_data, comm_data = mod_image.select_default_image()
    default_user_data = user_data
    default_community_data = comm_data
    app.run(host="jinrongdao.com", port=6100, processes=6)
