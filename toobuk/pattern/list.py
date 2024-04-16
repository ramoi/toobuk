from toobuk.pattern.abstract import *
import toobuk.util as ut


class Pattern(AbstractPattern):
    def _getResult_(self):
        return []

    def _makeUp_(self, pattern):
        for p in pattern:
            self._patternList_.append(PatternElement(p, self))


class PatternElement(AbstractPatternElement):

	def __init__(self, ptnEle, parent) :
		super().__init__(ptnEle, parent)
		self.skipper = self.__makeSkip__()

	def _makeUp_(self) :
		pass

	def __makeSkip__(self) :
		skipText = self._pattern_.get('skip')
		return Skipper(skipText)

	# def __makeSkip__(self) :
	# 	if not self._pattern_.get('skip') is None:
	# 		skip = self._pattern_.get('skip')
	# 		skipFunc = ut.getPlugin(skip)
	#
	# 		def skip(selectList, r) :
	# 			resultList = []
	# 			for select in selectList:
	# 				if not skipFunc(select.text, r):
	# 					resultList.append(select)
	#
	# 			return resultList
	#
	# 		return skip
	# 	if not self._pattern_.get('skip.value') is None:
	# 		def skip(selectList, r) :
	# 			resultList = []
	# 			for select in selectList:
	# 				if select.text != self._pattern_['skip.value']:
	# 					resultList.append(select)
	#
	# 			return resultList
	#
	# 		return skip
	# 	elif not self._pattern_.get('slice') is None:
	# 		slice = self._pattern_.get('slice')
	# 		if isinstance(slice, dict):
	# 			slice = [slice]
	#
	# 		def skip(selectList, r) :
	# 			resultList = []
	# 			for s in slice:
	# 				sp = s.get('start') or 0
	# 				ep = s.get('end') or len(selectList)
	# 				resultList = resultList + selectList[sp:ep]
	#
	# 			return resultList
	#
	# 		return skip
	# 	else :
	# 		return lambda select, r : select

	def apply(self, source, result):
		selectList = source.select(self._pattern_.get('selector'))
		resultList = self.skipper.skip(selectList, result)

		for index, select in enumerate(resultList):
			if len(result) < index + 1:
				result.append({})

			self._addData_(result[index], select)

def __slice__(sa):
	if isinstance(sa, dict):
		sa = [sa]
	def skip(selectList, r):
		resultList = []
		for s in sa:
			sp = s.get('start') or 0
			ep = s.get('end') or len(selectList)
			resultList = resultList + selectList[sp:ep]

		return resultList

	return skip


findx = 0
def __getFunc__(f) :
	print(str(++findx) + f.__name__)

	def skipF(selectList, r) :
		resultList = []
		for select in selectList:
			if not f(select.text, r) :
				resultList.append(select)

		return resultList

	return skipF

class Skipper :
	__skipper__:dict = {}
	__skipper__['white'] =  lambda text, r : text.isspace()
	__skipper__['slice'] =  __slice__

	C = re.compile(r'(?P<name>\w+(\.\w+)?)(?:\((?P<args>(\w+)=((([\'"]).+?\7)|[0-9.]+|\[.*\]|\{.*\}))+\))?')
	A = re.compile(r'(?P<key>\w+)=(?P<value>(([\'"]).*?\4)|[0-9.]+|\[.*\]|\{.*\})')

	@staticmethod
	def addSkipper(name, skipper) :
		Skipper.__skipper__[name] = skipper

	TYPE_STR = re.compile(r'([\'"])(?P<value>.*)\1')
	TYPE_FLOAT = re.compile(r'\d+.\d*?')
	TYPE_INT = re.compile(r'\d+?')

	@staticmethod
	def getValue(value) :
		m = Skipper.TYPE_STR.match(value)
		if not m is None :
			return m.group("value")

		m = Skipper.TYPE_FLOAT.match(value)
		if not m is None :
			return float(value)

		m = Skipper.TYPE_INT.match(value)
		if not m is None :
			return int(value)

		return ut.jsonToObj(value)

	@staticmethod
	def getSkipper(text) :
		if text is None :
			return None

		if Skipper.__skipper__.get(text) is None :
			module, conName = ut.getdinfo(text)

			mod = importlib.import_module(module)
			return getattr(mod, conName)
		else :
			return Skipper.__skipper__[text]
	def __init__(self, text):
		self.__list__ = []

		if not text is None :
			self.__initSkipper__(text)

	def __add__(self, skipper) :
		self.__list__.append(skipper)


	def __initSkipper__(self, text):
		self.text: str = text
		slist = Skipper.C.finditer(text)
		for s in slist:
			name = s.group("name")
			args = s.group("args")
			if args is None:
				self.__add__(__getFunc__(Skipper.getSkipper(name)))
			else:
				f = Skipper.getSkipper(name)
				argsList = Skipper.A.finditer(args)
				ka = {}
				for a in argsList:
					key = a.group("key")
					value = Skipper.getValue(a.group("value"))

					ka[key] = value

				self.__add__(f(**ka))

	def skip(self, selectList, result) :
		resultList = selectList
		for f in self.__list__ :
			print(f.__name__)
			resultList = f(resultList, result)

		return resultList


