from toobuk.conf import Configure
from toobuk.tb import Toobuk

if __name__ == '__main__' :
	t = Toobuk('statist/house/house.json')
	r = t.get( 'getDate' )
	print(r)
