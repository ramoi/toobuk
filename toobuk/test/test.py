from statist.stock.stock import *
from statist.currency.currency import *
from statist.debt.debt import *
from statist.house import house

def getStock() :
	s = StockProgress()
	resultData = s.grumble()

	print(resultData)


def m2() :
	s = Currency()
	resultData = s.grumble()

	print(resultData)

def governmentDebtRatioByGdp() :
	s = GovernmentDebtRatio()
	resultData = s.grumble()

	print(resultData)


def deptCp() :
	s = DebtCp()
	resultData = s.grumble()

	print(resultData)

def getLoc() :
	resultData = house.getLoc()
	print(resultData)

def getDate() :
	resultData = house.getDate()
	print(resultData)

def getTradeIDRatio() :
	resultData = house.getTradeIDRatio()
	print(resultData)


g = input('(1:stock, 2:currency, 3:debt, 4:house) : ')

if g is '1' :
	getStock()
elif g is '2' :
	m2()
elif g is '3' :
	print("TradeIDRatio............")
	governmentDebtRatioByGdp()
	deptCp()
elif g is '4' :
	getLoc()
	getDate()
	getTradeIDRatio()

