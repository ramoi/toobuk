from toobuk.tb import Toobuk

htb = Toobuk('test.json')
print( htb.get('getDate') )

class StockProgress(Toobuk) :
	def __init__(self) :
		self._walker = Toobuk('test.json')

	def grumble(self) :
		return self._walker.get('stock')  

s = StockProgress()
resultData = s.grumble()

print(resultData)

resultData = htb.get('stock', {'code': '005490'})  
print(resultData)

resultData = htb.get('getTradeIDRatio')
print(resultData)

