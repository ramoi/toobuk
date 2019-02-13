from toobuk.tb import Toobuk

class Currency(Toobuk):
	def __init__(self) :
		self._walker = Toobuk('statist/currency/currency.json')

	def grumble(self) :
		return self._walker.get('nation')