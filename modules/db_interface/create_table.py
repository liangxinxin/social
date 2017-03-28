# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask import jsonify
from flask import redirect, url_for

import os
import sys
sys.path.append(os.path.abspath('../..'))

from modules import mod_community
from modules import mod_login
from modules import mod_logout
from modules import mod_post
from modules import mod_reply
from modules import mod_user
from modules import mod_user_community
from modules import time_format
from modules.db_interface import db_model_user_relation
from modules.db_interface import db_default_image
from modules.db_interface import db_model_message_type
from modules.db_interface import db_model_message
from modules.db_interface import db_model_verify 
from modules.db_interface import db_model_comment
from modules.db_interface import db_model_reply
from modules.db_interface import db_model_user
from modules.db_interface import db_model_community
from modules.db_interface import db_model_post
from modules.db_interface import db_model_reply_like_stat
from modules.db_interface import db_model_user_community
from modules.db_interface import db_model_user_relation
from modules.db_interface import db_model_private_message


'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
# app.secret_key = "super secret key"
# app.config['SECRET_KEY'] = 'super secret key'
app.config.from_object('config')


'''  MAIN ENTRY  '''
if __name__ == '__main__':
    app.debug = True
    ##db_model_user_relation.create_table()
    print 'create table start'
    print 'create table default_image...'
    db_default_image.create_table()
    print 'create table user_relation...'
    db_model_user_relation.create_table()
    print 'create table message_type...'
    db_model_message_type.create_table()
    print 'insert value to table message_type...'
    db_model_message_type.insert_default_value()
    print 'create table message...'
    db_model_message.create_table()
    print 'create table verify...'
    db_model_verify.create_table()
    db_model_comment.create_table()
    db_model_reply.create_table()
    db_model_user.create_table()
    db_model_community.create_table()
    db_model_post.create_table()
    db_model_reply_like_stat.create_table()
    db_model_user_community.create_table()
    db_model_user_relation.create_table()
    db_model_private_message.create_table()
    print 'create table private message...'
    print 'create table end'

