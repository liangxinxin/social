import time
import re 
from flask import session

def service(request):
    result={}
    if request.method == 'POST':
        mobile = request.form.get("mobile")
        p=re.compile('1[3458]\\d{9}')
        match=p.match(mobile)
        if match:
          result['succ']='0'
          result['code']='0'
          result['message']='correct mobile '
        else:
          result['succ']='1'
          result['code']='2'
          result['message']=' not correct mobile'
    else:
        result['succ']='1'
        result['code']='1'
        result['message']=' not post method'
    return result;




