#coding=utf-8
import time
import json
from flask import session
from db_interface import db_model_private_message
from db_interface import  db_model_user

default_page_no=1
default_num_perpage = 10
def select_recent_user(request):
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        to_user_id =request.args.get('to_user_id',0)# after click private_mess btn
        user_list = [] # recent chat user
        unread_count_list = [] # unread message count
        if to_user_id>0:# have click private_mess
            to_user = db_model_user.select_by_id(to_user_id)
            user_list.append(to_user)
        page_no = request.args.get('page_no',default_page_no)
        num_perpage =request.args.get('num_perpage',default_num_perpage)
        to_user_list = db_model_private_message.select_recent_user(user_id)# 返回最近聊天的人
        for  user in to_user_list:
                #查询未读的消息条数
                count = db_model_private_message.select_unread_by_each_user(user.id,user_id)
                unread_count_list.append(int(count))
                if user not in user_list:
                    user_list.append(user)
        if len(user_list)>0 and to_user_id==0:
            to_user_id =user_list[0].id
        unread_count_list[0]=0 #第一个人不显示红色标注的未读消息条数
        user_num = len(user_list)
        return user_list,unread_count_list,user_num



def select_mess_by_user(request):
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        to_user_id = int(request.args.get('to_user_id', 0))  # after click user
        page_no = int(request.args.get('page_no', default_page_no))
        num_perpage = int(request.args.get('num_perpage', default_num_perpage))
        data = db_model_private_message.select_user_message(user_id,to_user_id,page_no,num_perpage)
        mess_list =[]
        for message in data:
            mess_list.append(db_model_private_message.to_json(message))
            if message.has_read==False:
                db_model_private_message.update_has_read(message.id)
        mess_list.reverse()
        return mess_list



def select_new_message(request):
    print 'into new mess'
    if session.get('userinfo'):
        to_user_id = int(session.get('userinfo')['id'])
        create_user_id = int(request.args.get('create_user_id'))
        new_messaage = db_model_private_message.select_new_message(create_user_id, to_user_id)
        mess_list = []
        for message in new_messaage:
            mess_list.append(db_model_private_message.to_json(message))
            db_model_private_message.update_has_read(message.id)
        # i=0
        # while (True):
        #     i=i+1
        #     mess_list=[]
        #     new_messaage = db_model_private_message.select_new_message(create_user_id, to_user_id)
        #     print 'new',new_messaage
        #     for message in new_messaage:
        #         message.has_read = True
        #         print 'pudate',message.has_read
        #         db_model_private_message.update_has_read(message)
        #         mess_list.append(db_model_private_message.to_json(message))
        #     if len(mess_list):
        #         break
        #
        #     print 'poll request',i
        #     time.sleep(5)
    return mess_list




def save_private_message(request):
    result={}
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        param = json.loads(request.form.get('data'))
        to_user_id = param['to_user_id']
        content = param['content']
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        message = db_model_private_message.insert(content,user_id,to_user_id,create_time)
        result['code']=0
        result['message']='success'
        result['data']= message
    else:
        result['code'] = 1
        result['message'] = 'fail'
        result['data'] = ''
    return result