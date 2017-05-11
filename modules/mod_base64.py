#encoding:utf-8
from bs4 import BeautifulSoup
import base64
import os
import time
import random
default_path = 'http://jinrongdao.com:6100/images/'

# base64 code convert to img src
# add by lxx 2017-04-10


def base64_hander(content, path_type):
    soup = BeautifulSoup(content,"html.parser")
    trs = soup.findAll("img")
    length = len(trs)
    print os.getcwd()
    cur_path = os.getcwd()
    print length
    for i in range(length):
        src = trs[i].attrs["src"].encode('utf-8')
        if src.startswith('data:image'):
            save_path = default_path + path_type + '/'
            upload_path = cur_path + '/static/images/' + path_type + '/'
            header = "data:image"
            cur_time = int(time.time())
            image_arr = src.split(",")
            end_index = image_arr[0].index(';')
            start_index = image_arr[0].index('/')
            file_type = src[start_index+1:end_index]
            print 'file_type',file_type
            rand1 = random.randint(0, 900) + 100
            rand2 = random.randint(0, 90) + 10
            file_name = '%s%s%s%s%s' % (cur_time, rand1, rand2,'.', file_type)
            save_path += file_name
            print('upload_path',upload_path,'file_name',file_name)
            if header in image_arr[0]:
                image = image_arr[1]
                try:
                    decoded_bytes = base64.decodestring(image)
                    if not os.path.exists(upload_path):
                        os.makedirs(upload_path)
                    upload_path += file_name
                    out = open(upload_path, 'w')
                    out.write(decoded_bytes)
                    out.close()
                    trs[i].attrs["src"] = save_path
                except Exception, e:
                    print 'base64_hander exception !',e
    soup = str(soup).replace('</img>','')
    return soup

