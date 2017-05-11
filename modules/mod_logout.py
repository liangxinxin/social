from flask import session


def service(request):
    result = {'succ': 1, 'code': 1, 'message': 'logout fail'}
    userinfo = session.get('userinfo')
    if userinfo is not None:
        session['userinfo'] = None
        result['succ'] = '0'
        result['code'] = '0'
        result['message'] = 'logout succ'
    return result
