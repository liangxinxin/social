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
default_path = 'http://0.0.0.0:6100/images/'


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
    curPath = os.getcwd()
    uploadPath = curPath + '/static/images/' + type + '/'
    oriFileName = request.form.get('filename').encode('utf-8')
    isDefault = request.form.get('isDefault').encode('utf-8')

    community_id = request.form.get('community_id', 0)
    print 'type' + type
    result = {}
    if isDefault == '1':
        savePath = default_path + type + '/default/' + oriFileName
        if type == 'user':
            db_model_user.save_head_image(user_id, savePath)
        elif type == 'community':
            db_model_community.save_head_image(community_id, savePath)
        message = "success"
        result = {"message": message, "code": 0}
    else:
        header = "data:image"
        curTime = int(time.time())  # time.mktime(datetime.datetime.now().timetuple())
        fileType = oriFileName[-4:]
        rand1 = random.randint(0, 900) + 100
        rand2 = random.randint(0, 90) + 10
        # curTime = time.mktime(datetime.datetime.now().timetuple())
        fileName = '%s%s%s%s' % (curTime, rand1, rand2, fileType)
        savePath = default_path + type + '/' + fileName
        print(fileName)
        image = request.form.get('image').encode('utf-8')
        imageArr = image.split(",")
        if header in imageArr[0]:
            image = imageArr[1]
            message = "fail"
            try:
                decodedBytes = base64.decodestring(image)
                if not os.path.exists(uploadPath):
                    os.makdirs(uploadPath)
                uploadPath = uploadPath + fileName
                out = open(uploadPath, 'w')
                out.write(decodedBytes)
                out.close()
                if type == 'user':
                    db_model_user.save_head_image(user_id, savePath)
                elif type == 'community':
                    db_model_community.save_head_image(community_id, savePath)
                message = "success"
                result = {"message": message, "code": 0}
                print("upload success")
            except Exception, e:
                result = {"message": message, "code": 1}

    return result


def select_default_image():
    # //type = request.args.get("type")
    # if type == "user":
    #     typeid = 0
    # else:
    #     typeid = 1
    user_json_result = []
    comm_json_result = []
    user_data = db_default_image.select_by_type(0, default_page_no, max_num_perpage).items
    comm_data = db_default_image.select_by_type(1, default_page_no, max_num_perpage).items
    if len(user_data) > 0:
        for object in user_data:
            jsonObj = db_default_image.to_json(object)
            user_json_result.append(jsonObj)
    if len(comm_data) > 0:
        for object in comm_data:
            jsonObj = db_default_image.to_json(object)
            comm_json_result.append(jsonObj)
    return user_json_result, comm_json_result
