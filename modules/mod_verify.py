import json
from flask import session
from db_interface import db_model_user
from db_interface import db_model_verify


def service(request):
    result = {}
    if request.method == 'POST':
        mobile = request.form['mobile']
        sms_code = request.form['sms_code']
    print "checks mscode , mobile and smscode is:", mobile, sms_code
    # check if user exist
    data = db_model_user.select_by_mobile(mobile)
    if data:
        print "user have exist!"
        result['succ'] = '1'
        result['code'] = '1'
        result['message'] = 'use exist!'
    else:
        # check if mobile and smscode correct
        if sms_code == '123456':
            print "is ok code"
            result['succ'] = '0'
            result['code'] = '0'
            result['message'] = 'regist succ!'
            session['userinfo'] = {'mobile': mobile}
            print 'verify pass!----', result, session
        else:
            verify_data = db_model_verify.select_by_mobile_and_sms_code(mobile, sms_code)
            if verify_data:
                print "verify succ!"
                result['succ'] = '0'
                result['code'] = '0'
                result['message'] = 'regist succ!'
                session['user_info'] = {'mobile': mobile}
            else:
                print " verify fail"
                result['succ'] = '1'
                result['code'] = '2'
                result['message'] = 'verify code is not correct'


    return result
