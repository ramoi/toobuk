from toobuk.tb import Toobuk

htb = Toobuk('test')
# print( htb.get('housetrade/date') )
# print('------------------------------------------------------------------')
# print( htb.get('housetrade') )
# print('------------------------------------------------------------------')

# resultData = htb.get('stock', {'code': '005490'})  
# print(resultData)

# print('------------------------------------------------------------------')

resultData = htb.get('bok')
print(resultData)

# resultData = htb.get('stockDetail')  
# print(resultData)


data = resultData.get('currList')
for d in data :
	print(d['년월'], ',', d['본원통화'])


aa