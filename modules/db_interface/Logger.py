# coding=utf-8
import datetime
import logging


# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger():
    def __init__(self, logname, loglevel, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''

        format = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
        curDate = datetime.date.today() - datetime.timedelta(days=0)
        infoLogName = r'/Users/liangxinxin/Desktop/info_%s.log' % curDate
        errorLogName = r'/Users/liangxinxin/Desktop/error_%s.log' % curDate

        formatter = logging.Formatter(format)

        self.infoLogger = logging.getLogger("infoLogger")
        self.errorLogger = logging.getLogger("errorLogger")

        self.infoLogger.setLevel(logging.INFO)
        self.errorLogger.setLevel(logging.ERROR)

        infoHandler = logging.FileHandler(infoLogName, 'a')
        infoHandler.setLevel(logging.INFO)
        infoHandler.setFormatter(formatter)

        errorHandler = logging.FileHandler(errorLogName, 'a')
        errorHandler.setLevel(logging.ERROR)
        errorHandler.setFormatter(formatter)

        testHandler = logging.StreamHandler()
        testHandler.setFormatter(formatter)
        testHandler.setLevel(logging.ERROR)

        self.infoLogger.addHandler(infoHandler)
        self.infoLogger.addHandler(testHandler)
        self.errorLogger.addHandler(errorHandler)


