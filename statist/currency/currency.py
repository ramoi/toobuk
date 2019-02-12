from toobuk.conf import Configure
from toobuk.tb import Toobuk
import re,toobuk.util as util


class CurrencyToobuk(Toobuk) :
	def _setJson(self) :
		conf = Configure('statist/currency', 'currency.json')
		self.__json__ = conf.getJson()

class IncreatRatioByNation(CurrencyToobuk) :

	def grumble(self) :
		json = self.getJson()

		result = self.get( json.get('nation') )

		return result