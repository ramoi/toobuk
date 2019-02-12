from toobuk.conf import Configure
from toobuk.tb import Toobuk
import re,toobuk.util as util

class HouseToobuk(Toobuk) :
	def _setJson(self) :
		conf = Configure('statist/house', 'house.json')
		self.__json__ = conf.getJson()

htb = HouseToobuk()
json = htb.getJson()


def getDate() :
	return htb.get(json.get('getDate'))

def getLoc() :
	return htb.get(json.get('getLoc'))

def getTradeIDRatio() :
	return htb.get(json.get('getTradeIDRatio'))

