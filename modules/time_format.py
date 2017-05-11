# -*- coding: utf-8 -*-
import time
import math
import datetime


def timestampFormat(timestampParam):
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    timestamp = time.mktime(time.strptime(str(timestampParam), ISOTIMEFORMAT))
    curTimestamp = time.mktime(datetime.datetime.now().timetuple())  # 当前时间戳
    timestampDiff = curTimestamp - timestamp  # 参数时间戳与当前时间戳相差秒数

    cur_date = time.localtime()  # 当前时间日期对象
    tm_date = time.strptime(str(timestampParam), ISOTIMEFORMAT)  # 参数时间戳转换成的日期对象

    Y = tm_date.tm_year
    m = tm_date.tm_mon
    d = tm_date.tm_mday
    H = tm_date.tm_hour
    i = tm_date.tm_min
    s = tm_date.tm_sec
    if i >= 0 and i < 10:
        i = '0' + str(i)
    if timestampDiff < 60:  # 一分钟以内
        return "刚刚"
    elif timestampDiff < 3600:  # 一小时前之内
        return str(int(math.floor(timestampDiff / 60))) + "分钟前"
    elif cur_date.tm_year == Y and cur_date.tm_mon == m and cur_date.tm_mday == d:
        return '今天' + str(H) + ':' + str(i)
    else:
        newDate = time.localtime((timestamp - 86400))  # 参数中的时间戳加一天转换成的日期对象

    if newDate.tm_year == Y and newDate.tm_mon == m and newDate.tm_mday == d:
        return '昨天' + str(H) + ':' + str(i)
    elif cur_date.tm_year == Y:
        return str(m) + '月' + str(d) + '日 ' + str(H) + ':' + str(i)
    else:
        return str(Y) + '年' + str(m) + '月' + str(d) + '日 ' + str(H) + ':' + str(i)
