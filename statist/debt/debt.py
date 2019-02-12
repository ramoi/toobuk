from toobuk.conf import Configure
from toobuk.tb import Toobuk
import re,toobuk.util as util

class DebtToobuk(Toobuk) :
	def _setJson(self) :
		conf = Configure('statist/debt', 'debt.json')
		self.__json__ = conf.getJson()


class GDebtRation(DebtToobuk) :
	def grumble(self) :
		json = self.getJson()
		return self.get( json.get('goernmentDebtRatio') )

class DeptComposition(DebtToobuk) :
	def grumble(self) :
		json = self.getJson()
		return self.get( json.get('debtCp') )
