# coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db


class DefaultImage(db.Model):
    __tablename__ = 'default_image'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(2), unique=False)
    imgsrc = db.Column(db.String(100), unique=False)

    def __init__(self, imgsrc, type):
        self.type = type
        self.imgsrc = imgsrc


def create_table():
    db.create_all()


def select_by_type(typeid, page_no, num_per_page):
    paginate = DefaultImage.query.filter_by(type=typeid).paginate(page_no, num_per_page, False)
    return paginate


def to_json(object):
    if isinstance(object, DefaultImage):
        return {
            'id': object.id,
            'type': object.type,
            'imgsrc': object.imgsrc
        }

def create_default_user_img():
    sql="INSERT INTO `default_image` (`id`, `type`, `imgsrc`) VALUES\
	(1,'0','http://jinrongdao.com:6100/images/user/img1.jpg'),\
	(2,'0','http://jinrongdao.com:6100/images/user/img2.jpg'),\
	(3,'0','http://jinrongdao.com:6100/images/user/img3.jpg'),\
	(4,'0','http://jinrongdao.com:6100/images/user/img4.jpg'),\
	(5,'0','http://jinrongdao.com:6100/images/user/img5.jpg'),\
	(6,'0','http://jinrongdao.com:6100/images/user/img6.jpg'),\
	(7,'0','http://jinrongdao.com:6100/images/user/img7.jpg'),\
	(8,'0','http://jinrongdao.com:6100/images/user/img8.jpg'),\
	(9,'0','http://jinrongdao.com:6100/images/user/img9.jpg'),\
	(10,'0','http://jinrongdao.com:6100/images/user/img10.jpg'),\
	(11,'0','http://jinrongdao.com:6100/images/user/img11.jpg'),\
	(12,'0','http://jinrongdao.com:6100/images/user/img12.jpg'),\
	(13,'0','http://jinrongdao.com:6100/images/user/img13.jpg'),\
	(14,'0','http://jinrongdao.com:6100/images/user/img14.jpg'),\
	(15,'0','http://jinrongdao.com:6100/images/user/img15.jpg'),\
	(16,'0','http://jinrongdao.com:6100/images/user/img16.jpg'),\
	(17,'0','http://jinrongdao.com:6100/images/user/img17.jpg'),\
	(18,'0','http://jinrongdao.com:6100/images/user/img18.jpg'),\
	(19,'0','http://jinrongdao.com:6100/images/user/img19.jpg'),\
	(20,'0','http://jinrongdao.com:6100/images/user/img20.jpg'),\
	(21,'0','http://jinrongdao.com:6100/images/user/img21.jpg'),\
	(22,'0','http://jinrongdao.com:6100/images/user/img22.jpg'),\
	(23,'0','http://jinrongdao.com:6100/images/user/img23.jpg'),\
	(24,'0','http://jinrongdao.com:6100/images/user/img24.jpg'),\
	(25,'0','http://jinrongdao.com:6100/images/user/img25.jpg')"
    db.session.execute(sql)

def create_default_community_img():
    sql="INSERT INTO `default_image` (`id`, `type`, `imgsrc`) VALUES\
	(26,'1','http://jinrongdao.com:6100/images/shequ/img1.jpg'),\
	(27,'1','http://jinrongdao.com:6100/images/shequ/img2.jpg'),\
	(28,'1','http://jinrongdao.com:6100/images/shequ/img3.jpg'),\
	(29,'1','http://jinrongdao.com:6100/images/shequ/img4.jpg'),\
	(30,'1','http://jinrongdao.com:6100/images/shequ/img5.jpg'),\
	(31,'1','http://jinrongdao.com:6100/images/shequ/img6.jpg'),\
	(32,'1','http://jinrongdao.com:6100/images/shequ/img7.jpg'),\
	(33,'1','http://jinrongdao.com:6100/images/shequ/img8.jpg'),\
	(34,'1','http://jinrongdao.com:6100/images/shequ/img9.jpg'),\
	(35,'1','http://jinrongdao.com:6100/images/shequ/img10.jpg'),\
	(36,'1','http://jinrongdao.com:6100/images/shequ/img11.jpg'),\
	(37,'1','http://jinrongdao.com:6100/images/shequ/img12.jpg'),\
	(38,'1','http://jinrongdao.com:6100/images/shequ/img13.jpg'),\
	(39,'1','http://jinrongdao.com:6100/images/shequ/img14.jpg'),\
	(40,'1','http://jinrongdao.com:6100/images/shequ/img15.jpg'),\
	(41,'1','http://jinrongdao.com:6100/images/shequ/img16.jpg'),\
	(42,'1','http://jinrongdao.com:6100/images/shequ/img17.jpg'),\
	(43,'1','http://jinrongdao.com:6100/images/shequ/img18.jpg'),\
	(44,'1','http://jinrongdao.com:6100/images/shequ/img19.jpg'),\
	(45,'1','http://jinrongdao.com:6100/images/shequ/img20.jpg'),\
	(46,'1','http://jinrongdao.com:6100/images/shequ/img21.jpg'),\
	(47,'1','http://jinrongdao.com:6100/images/shequ/img22.jpg')"
    db.session.execute(sql)
