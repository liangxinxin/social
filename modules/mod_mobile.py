import re

from db_interface import db_model_user
from Logger import *


def service(request):
    result = {}
    if request.method == 'POST':
        operate_type = request.form.get("type")
        mobile = request.form.get("mobile")
        if operate_type == 'check_exist':
            user = db_model_user.select_by_mobile(mobile)
            if user is not None:
                result['succ'] = '0'
                result['code'] = '0'
                result['message'] = 'correct mobile '
            else:
                result['succ'] = '1'
                result['code'] = '1'
                result['message'] = 'mobile not exist'
        else:
            p = re.compile('1[3458]\\d{9}')
            match = p.match(mobile)
            if match:
                result['succ'] = '0'
                result['code'] = '0'
                result['message'] = 'correct mobile '
            else:
                result['succ'] = '1'
                result['code'] = '2'
                result['message'] = ' not correct mobile'
    else:
        result['succ'] = '1'
        result['code'] = '1'
        result['message'] = ' not post method'
    Logger.infoLogger.info('result code: %s,message %s',result['code'],result['message'])
    return result
