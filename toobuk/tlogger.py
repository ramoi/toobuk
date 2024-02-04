import logging
import logging.config
import os
import os.path

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
            logging.config.fileConfig(TLoggerFactory.conf['file'])
            return TLoggerFactory.getTLogger(TLoggerFactory.conf['name'])


    @classmethod
    def getEmptyLogger(cls):
        if not cls.__emptyLogger__ is None :
            return cls.__emptyLogger__

        # create logger
        __emptyLogger__ = EmptyLogger()

        return __emptyLogger__

    @classmethod
    def getTLogger(cls, name):
        return TLogger.getLogger(name)

class TLogger:
    __logger__ = {}

    @staticmethod
    def getLogger(name):
        if name not in TLogger.__logger__ :
            logger = logging.getLogger(name)
            print('logger=============================================>', logger)
            if logger is None:
                print("logger is None")
                return

            TLogger.__logger__[name] = logger

        return TLogger.__logger__[name]

class EmptyLogger :
    def debug(self, msg, *args, **kwargs):
        None

    def info(self, msg, *args, **kwargs):
        None

    def warning(self, msg, *args, **kwargs):
        None

    def error(self, msg, *args, **kwargs):
        None

    def critical(self):
        None