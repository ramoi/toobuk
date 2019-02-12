from toobuk.conf import Configure
from toobuk.tb import Toobuk
import re,toobuk.util as util

class HouseToobuk(Toobuk) :
	def _setJson(self) :
		conf = Configure('statist/house', 'house.json')
		self.__json__ = conf.getJson()

anlyzer = HouseToobuk()
json = anlyzer.getJson()


def getDate() :
	return anlyzer.get(json.get('getDate'))

def getLoc() :
	return anlyzer.get(json.get('getLoc'))

def getTradeIDRatio() :
	return anlyzer.get(json.get('getTradeIDRatio'))

