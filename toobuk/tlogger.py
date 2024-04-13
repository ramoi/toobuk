import logging
import logging.config
import os
import os.path
import http.client

http.client.HTTPConnection.debuglevel = 1

class TLoggerFactory :
    __logger__ = {}
    __emptyLogger__ = None

    conf = {
        "file" : 'tlogger.conf',
        "name" : 'toobuk'
    }

    @classmethod
    def getLogger(cls):

        if not os.path.isfile(TLoggerFactory.conf['file']) :
            print("empty logger===========================>", TLoggerFactory.conf['file'])
            return TLoggerFactory.getEmptyLogger()
        else :
            print("exist logger===========================>", TLoggerFactory.conf['file'])
            # logging.config.fileConfig(TLoggerFactory.conf['file'])
            logger = TLoggerFactory.getTLogger()
            return logger


    @classmethod
    def getEmptyLogger(cls):
        if not cls.__emptyLogger__ is None :
            return cls.__emptyLogger__

        # create logger
        __emptyLogger__ = EmptyLogger()

        return __emptyLogger__

    @classmethod
    def getTLogger(cls):
        return TLogger.getLogger()

class TLogger:
    __logger__ = {}

    @staticmethod
    def getLogger():
        name = TLoggerFactory.conf['name']
        if name not in TLogger.__logger__ :
            logging.config.fileConfig(TLoggerFactory.conf['file'])
            logger = logging.getLogger(name)
            if logger is None:
                print("logger is None")
                return

            TLogger.__logger__[name] = logger

        return TLogger.__logger__[name]

class EmptyLogger :
    def debug(self, msg, *args, **kwargs):
        print('logging not set')

    def info(self, msg, *args, **kwargs):
        print('logging not set')

    def warning(self, msg, *args, **kwargs):
        print('logging not set')

    def error(self, msg, *args, **kwargs):
        print('logging not set')

    def critical(self):
        print('logging not set')
