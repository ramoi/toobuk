import json, os, re

def getJson(dir, jsonName) :
	jsonTuple = None
	with open(os.path.join(dir, jsonName) ) as f : 
		jsonTuple = json.loads( f.read() )

	return jsonTuple

if __name__ == "__main__" :
	#stockJson = json.loads(open('stock.json').read())
	stockJson = getJson('.', 'stock.json')

class CofigureError(Exception) :
	pass

class Configure :
	def __init__(self, dir, name) :
		self.__load__(dir, name)
		self.__restructure__()

	def __load__(self, dir, name) :
		jsonTuple = None
		print (os.path.join(dir, name));
		with open(os.path.join(dir, name) ) as f : 
			jsonTuple = json.loads( f.read() )

		self.__json__ = jsonTuple

	def __restructure__(self) :
		for key in self.__json__.keys() :
			self.__setRegx__(self.__json__[key]['output'].get('list' ) )
			self.__setRegx__(self.__json__[key]['output'].get('single') )

	def __setRegx__(self, patternList ) :
		if patternList is None : 
			return

		for pattern in patternList :
			if not pattern.get('regx') is None :
				pattern['regx']['re'] = re.compile(pattern['regx']['pattern'])

	def getJson(self) : 
		return self.__json__

