#!/usr/bin/python
#coding=utf-8
import sys

from flask import Flask
from MySQLAlchemy import *

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask('__main__', static_url_path='')
#connect db params,please change it to your own,format:  db_type/user:password@ip/database   .........
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/social'
app.config['SECRET_KEY'] = '}\x94\xf6v\xb5\x9f\x86\xea$>\xaa\xd3\xc3\x99\xe9\xe0\xdbR\x1b\xda\x05\x87\xf8N'
db = MySQLAlchemy(app)
