# coding=utf-8

from flask import session
from db_interface import db_model_comment
from db_interface import db_model_message
from db_interface import db_model_private_message
from db_interface import  db_model_message_type ##勿删除，否则加载不到 message_type

default_page_no = 1
default_num_perpage = 10


def service(request):
    print 'enter do db_model_message  service'
    if request.method == 'GET':
        type = request.args.get('type')
        if type == 'query':
            return select_comment_message(request)


def select_comment_message(request):
    if session.get('userinfo'):
        to_userid = session.get('userinfo')['id']
        message_type = int(request.args.get('message_type', 3))  # 1.guanzhu 2.zan 3.pinglun 4.huifu
        page_no = int(request.args.get('no', default_page_no))
        num_perpage = int(request.args.get('size',default_num_perpage))
        read_list, unread_list = db_model_message.select_message_by_to_user(message_type, to_userid, page_no,
                                                                            num_perpage)
        total = read_list.total
        if message_type == 4:
            for message in read_list.items:
                comment = message.comment
                if comment.parent_id:
                    comment.parent = db_model_comment.select_by_id(comment.parent_id)
                    # message.comment = comment
            for message in unread_list:
                db_model_message.update_has_read(message.id, True)
                comment = message.comment
                if comment.parent_id:
                    comment.parent = db_model_comment.select_by_id(comment.parent_id)
                    # message.comment = comment
        else:
            for message in unread_list:
                db_model_message.update_has_read(message.id, True)
        print "query message type--------------:", message_type, " num:", len(read_list.items)
        return read_list.items, unread_list, total, page_no, num_perpage, message_type


def select_unread_num_by_type():
    mess_dict = {}
    if session.get('userinfo'):
        userid = session.get('userinfo')['id']
        private_unread_count = db_model_private_message.select_all_unread(userid)
        count_comment, count_reply, count_guanzhu, count_do_good = db_model_message.select_num_unread_by_type(False,
                                                                                                              userid)
        mess_dict['comment'] = count_comment
        mess_dict['reply'] = count_reply
        mess_dict['guanzhu'] = count_guanzhu
        mess_dict['zan'] = count_do_good
        mess_dict['sixin'] = private_unread_count
    return mess_dict
