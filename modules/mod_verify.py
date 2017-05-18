import json
from flask import session
from db_interface import db_model_user
from db_interface import db_model_verify
from Logger import *


def service(request):
    result = {}
    if request.method == 'POST':
        mobile = request.form['mobile']
        sms_code = request.form['sms_code']
    Logger.infoLogger.info('checks mscode , mobile and smscode is:%s,%s',mobile, sms_code)
    # check if user exist
    data = db_model_user.select_by_mobile(mobile)
    if data:
        result['succ'] = '1'
        result['code'] = '1'
        result['message'] = 'use exist!'
        Logger.infoLogger.error('result:%s',result)
    else:
        # check if mobile and smscode correct
        if sms_code == '123456':
            result['succ'] = '0'
            result['code'] = '0'
            result['message'] = 'regist succ!'
            session['userinfo'] = {'mobile': mobile}
            Logger.infoLogger.info('result:%s,session:%s', result,session['userinfo'])
        else:
            verify_data = db_model_verify.select_by_mobile_and_sms_code(mobile, sms_code)
            if verify_data:
                result['succ'] = '0'
                result['code'] = '0'
                result['message'] = 'regist succ!'
                session['user_info'] = {'mobile': mobile}
                Logger.infoLogger.info('result:%s,session:%s', result,session['userinfo'])
            else:
                result['succ'] = '1'
                result['code'] = '2'
                result['message'] = 'verify code is not correct'
                Logger.infoLogger.error('result:%s', result)

    return result
