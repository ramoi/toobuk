import json, os, re

def getJson(dir, jsonName) :
	jsonTuple = None
	with open(os.path.join(dir, jsonName) ) as f : 
		jsonTuple = json.loads( f.read() )

	return jsonTuple

class CofigureError(Exception) :
	pass

class Configure :
	def __init__(self, path) :
		self.__load__(path)
		self.__restructure__()

	def __load__(self, path) :
		jsonTuple = None
		#with open(os.path.join(dir, name) ) as f : 
		with open( path ) as f : 
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


if __name__ == "__main__" :
	#stockJson = json.loads(open('stock.json').read())
	stockJson = getJson('.', 'stock.json')
