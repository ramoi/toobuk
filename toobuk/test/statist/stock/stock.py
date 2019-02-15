from toobuk.tb import Toobuk

class StockProgress(Toobuk) :
	def __init__(self) :
		self._walker = Toobuk('statist/stock/stock.json')

	def grumble(self) :
		stock = self._walker.get('stock') 
		cmpr = self._walker.get("cmpr") 

		return { 'stock' : stock, 'cmpr' : cmpr }

