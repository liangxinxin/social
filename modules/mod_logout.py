from flask import session

def service(request):
  model = {}
  userinfo = session.get('userinfo')
  next_url=request.args.get('next_url')
  if userinfo is not None:
    session['userinfo'] = None
  return model,next_url
