from abc import *

import requests
from bs4 import BeautifulSoup
from toobuk.tlogger import TLoggerFactory
import toobuk.util as ut

logger = TLoggerFactory.getLogger()

class AbstractConnector(metaclass=ABCMeta):
    def __init__(self, json):
        self._json_ = json
        self._bsType_ = ut.JsonConf.BS_TYPE.get(json, 'bs.type')
        self._encoding_ = ut.JsonConf.BS_ENCODING.get(json, 'encoding')

        self.__idx__ = 0

    def getUrl(self, parameter):
        return parameter.replaceUrl(self._json_['url'])

    def beforeConnect(self, headers, parameter):
        pass

    def afterConnect(self, bs):
        return bs

    def get(self, headers, parameter):
        url = self.getUrl(parameter)
        logger.debug('connect url=======>' + url)

        self.beforeConnect(headers, parameter)
        bs = self.connect(url, headers, parameter)
        bs = self.afterConnect(bs)

        return {'source': bs, 'parameter': parameter}

    @abstractmethod
    def connect(self, url, headers, parameter):
        pass


class GetConnector(AbstractConnector):

    def connect(self, url, headers, parameter):
        html = requests.get(url, headers=headers)
        logger.debug(html.status_code)
        logger.debug('===============================' + self._bsType_ + '====' + self._encoding_)
        logger.debug(html.encoding)

        bs = BeautifulSoup(html.content, self._bsType_, from_encoding=self._encoding_)

        return bs


class PostConnector(AbstractConnector):

    def getUrl(self, parameters):
        return self._json_['url']

    def connect(self, url, headers, parameter):
        html = requests.post(url, headers=headers, data=parameter.getData())
        logger.debug(html.status_code)
        bs = BeautifulSoup(html.text, self._bsType_, from_encoding=self._encoding_ )

        return bs