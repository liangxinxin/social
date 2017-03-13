from flask import session

def service(request):
  result = {}
  result['succ'] = '1'
  result['code'] = '1'
  result['message'] = 'logout fail'
  userinfo = session.get('userinfo')
  if userinfo is not None:
    session['userinfo'] = None
    result['succ'] = '0'
    result['code'] = '0'
    result['message'] = 'logout succ'
  return result 
