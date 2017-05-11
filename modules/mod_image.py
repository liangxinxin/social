import base64
import os
import random
import time

from flask import session

from db_interface import db_default_image
from db_interface import db_model_user
from db_interface import db_model_community

default_page_no = 1
default_num_perpage = 20
default_community_id = 0
default_post_id = 0
default_relation = 0
has_relation = 1
cancel_relation = 2
default_relation_id = 0
max_num_perpage = 100
default_path = 'http://jinrongdao.com:6100/images/'


def service(request):
    print "enter do user create service"
    if request.method == 'POST':
        return upload_head_image(request)
    elif request.method == 'GET':
        return select_default_image(request)


def upload_head_image(request):
    user_id = session.get('userinfo')['id']
    type = request.form.get("type")  # user/community
    print os.getcwd()
    cur_path = os.getcwd()
    ori_file_name = request.form.get('filename').encode('utf-8')
    is_default = request.form.get('isDefault').encode('utf-8')
    community_id = request.form.get('community_id', 0)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    print 'type',type
    result = {}
    if is_default=='true':
        savePath = default_path + type + '/' + ori_file_name
        if type == 'user':
            db_model_user.save_head_image(user_id, savePath)
        elif type == 'shequ':
            db_model_community.save_head_image(community_id, savePath,update_time)
        elif type == 'createShequ':
            savePath = default_path + 'shequ' + '/' + ori_file_name
        print 'upload image type',type
        message = "success"
        result = {"message": message, "code": 0,"data":savePath}
    else:
        print 'do upload_head_image'
        upload_path = cur_path + '/static/images/upload/' + type + '/'
        header = "data:image"
        curTime = int(time.time())  # time.mktime(datetime.datetime.now().timetuple())
        fileType = ori_file_name[-4:]
        rand1 = random.randint(0, 900) + 100
        rand2 = random.randint(0, 90) + 10
        print 'random',rand1, rand2
        file_name = '%s%s%s%s' % (curTime, rand1, rand2, fileType)
        save_path = default_path +'upload/'+ type + '/' + file_name
        print 'savePath', save_path,
        print 'uploadPath', upload_path
        print' fileName', file_name
        image = request.form.get('image').encode('utf-8')
        image_arr = image.split(",")
        print 'imageArr[0]',image_arr[0]
        if header in image_arr[0]:
            image = image_arr[1]
            message = "fail"
            try:
                decoded_bytes = base64.decodestring(image)
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                upload_path += file_name
                out = open(upload_path, 'w')
                out.write(decoded_bytes)
                out.close()
                if type == 'user':
                    db_model_user.save_head_image(user_id, save_path)
                elif type == 'shequ':
                    db_model_community.save_head_image(community_id, save_path, update_time)
                message = "success"
                result = {"message": message, "code": 0,"data":save_path}
                print("upload success")
            except Exception, e:
                result = {"message": message, "code": 1,"data":''}
                print e

    return result


def select_default_image():
    user_json_result = []
    comm_json_result = []
    user_data = db_default_image.select_by_type(0, default_page_no, max_num_perpage).items
    comm_data = db_default_image.select_by_type(1, default_page_no, max_num_perpage).items
    if len(user_data) > 0:
        for object in user_data:
            json_user = db_default_image.to_json(object)
            user_json_result.append(json_user)
    if len(comm_data) > 0:
        for object in comm_data:
            json_comm = db_default_image.to_json(object)
            comm_json_result.append(json_comm)
    return user_json_result, comm_json_result
