#from abc import *
from toobuk.conf import Configure, DataSet
import re


# class Toobuk(metaclass=ABCMeta) :
class Toobuk :

    def __init__(self, path) :
        self.__conf__ = Configure.get(path)

    @staticmethod
    def __toArray__( s ) :
        return s.split('&') if s else s

    __PATH_REG__ = re.compile(r'^(?P<name>.+?)(/(?P<output>.*))?$')

    @staticmethod
    def getPathInfo(path) :
        return Toobuk.__PATH_REG__.search(path)

    def get(self, path, parameter=None, headers=None, looopJson=None) :
        return self.grumble(path, parameter, headers, looopJson)


    def grumble(self, path, parameter=None, headers=None, looopJson=None) :
        pathInfo = Toobuk.getPathInfo(path)

        connMgr = self.__conf__.getConnectManager(pathInfo.group('name'))
        outputPath = Toobuk.__toArray__(pathInfo.group('output'))

        return connMgr.get(outputPath, parameter, headers, looopJson)