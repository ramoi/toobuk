from toobuk.conf import Configure
from toobuk.tb import Toobuk
import re,toobuk.util as util

class StockToobuk(Toobuk) :
	def _setJson(self) :
		conf = Configure('statist/stock', 'stock.json')
		self.__json__ = conf.getJson()

class StockProgress(StockToobuk) :
	def grumble(self) :
		json = self.getJson()

		stock = self.get( json.get('stock') )
		cmpr = self.get( json.get("cmpr") )

		return { 'stock' : stock, 'cmpr' : cmpr }



if __name__ == '__main__' :
	s = StockToobuk()
	s.get()