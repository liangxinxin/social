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
from modules.db_interface import db_model_message_type
from modules.db_interface import db_model_message

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
# app.secret_key = "super secret key"
# app.config['SECRET_KEY'] = 'super secret key'
app.config.from_object('config')


'''  MAIN ENTRY  '''
if __name__ == '__main__':
    app.debug = True
    db_model_user_relation.create_table()
    db_model_message_type.create_table()
    db_model_message.create_table()

