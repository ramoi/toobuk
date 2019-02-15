from toobuk.tb import Toobuk

htb = Toobuk('statist/house/house.json')

def getDate() :
	return htb.get('getDate')

def getLoc() :
	return htb.get('getLoc')

def getTradeIDRatio() :
	return htb.get('getTradeIDRatio')

