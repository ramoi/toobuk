from abc import *

import requests
from bs4 import BeautifulSoup
from toobuk.tlogger import TLoggerFactory
import toobuk.util as ut

logger = TLoggerFactory.getLogger()

class AbstractConnector(metaclass=ABCMeta):
    def __init__(self, headers, parameter, json):
        self._headers_ = headers
        self._parameter_ = parameter

        self._json_ = json
        self._bsType_ = ut.JsonConf.BS_TYPE.get(json, 'bs.type')
        self._encoding_ = ut.JsonConf.BS_ENCODING.get(json, 'encoding')

        self.__idx__ = 0

    def isFirst(self):
        return self.__idx__ == 0

    def hasMoreConnect(self):
        return self.__idx__ < len(self._parameter_)

    def getHeaders(self):
        return self._headers_

    def getParameter(self):
        parameter = self._parameter_[self.__idx__]
        self.__idx__ = self.__idx__ + 1
        return parameter

    def getUrl(self, parameter):
        return parameter.replaceUrl(self._json_['url'])

    def beforeConnect(self):
        pass

    def afterConnect(self, bs):
        return bs

    def get(self):
        parameter = self.getParameter()
        url = self.getUrl(parameter)
        logger.debug('connect url=======>' + url)

        self.beforeConnect()
        bs = self.connect(url, parameter)
        bs = self.afterConnect(bs)

        return {'source': bs, 'parameter': parameter}

    @abstractmethod
    def connect(self, url, parameter):
        pass


class GetConnector(AbstractConnector):

    def connect(self, url, parameter):
        html = requests.get(url, headers=self._headers_)
        logger.debug(html.status_code)
        logger.debug('===============================' + self._bsType_ + '====' + self._encoding_)
        logger.debug(html.encoding)

        bs = BeautifulSoup(html.content, features='html.parser', from_encoding='UTF-8')

        return bs


class PostConnector(AbstractConnector):

    def getUrl(self, parameters):
        return self._json_['url']

    def connect(self, url, parameter):
        html = requests.post(url, headers=self._headers_, data=self._prameter_.getData())
        logger.debug(html.status_code)
        bs = BeautifulSoup(html.text, self._bsType_, from_encoding=self._encoding_ )

        return bs