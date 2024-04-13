import importlib
from abc import *
import re
import toobuk.util as ut


TYPE_SWITCHER = {
	"int" : int,
	"float": float
}

class AbstractPattern(metaclass=ABCMeta) :
	def __init__(self, pattern, parent) :
		self._parent_ = parent
		self._patternList_ = []

		self._makeUp_(pattern)

	def getParent(self) :
		return self._parent_

	def apply(self, source ) :
		result = self._getResult_()
		self._applyPattern_(source, result)
		return result

	def _applyPattern_(self, source, result) :
		for pe in self._patternList_ :
			pe.apply(source, result)

		return result

	@abstractmethod
	def _makeUp_(self, pattern) :
		pass

	@abstractmethod
	def _getResult_(self) :
		pass

class AbstractPatternElement(metaclass=ABCMeta) :

	def __init__(self, ptnEle, parent) :
		self._parent_ = parent
		self._pattern_ = ptnEle
		self._type_ = parent.getParent().getJson()['type']

		self.converter = self.__makeConverter__()
		self.skip = None

		self._makeUp_()

	def __makeConverter__(self) :
		converterText = self._pattern_.get('converter')
		return Converter(converterText)

	# def __makeConveter__(self) :
	# 	ptnEle = self._pattern_
	# 	t = ptnEle.get('type')
	# 	converter = AbstractPatternElement.getConverer(ptnEle.get('converter'))
	#
	# 	if converter :
	# 		return converter
	# 	elif not ptnEle.get('regx') is None :
	# 		regx = re.compile(ptnEle['regx']['pattern'])
	# 		replace = ptnEle['regx']['replace']
	#
	# 		if t is None :
	# 			return lambda text, r : regx.sub( replace, text )
	# 		else :
	# 			return lambda text, r : TYPE_SWITCHER[t]( regx.sub( replace, text ) )
	# 	else :
	# 		if t is None :
	# 			return lambda text, r : text
	# 		else :
	# 			return lambda text, r : TYPE_SWITCHER[t]( text )

	def _addData_(self, r, select) :
		r[self._pattern_['name']] = self.converter.convert(select.text, r)

	@abstractmethod
	def _makeUp_(self):
		pass

	@abstractmethod
	def apply( self, source, result ) :
		pass

class Converter :
	__converter__:dict = {}
	__converter__['currency'] =  lambda text, r : re.compile(r'\B(?=(\d{3})+(?=\D|$))').sub(',', text)
	__converter__['remove.comma'] = lambda text, r : re.compile(r',').sub('', text)
	__converter__['int'] = lambda text, r : int(text)
	__converter__['float'] = lambda text, r : float(text)
	__converter__['regx'] = ut.regConverter

	C = re.compile(r'(?P<name>\w+(\.\w+)?)(?:\((?P<args>(\w+)=((([\'"]).+?\7)|[0-9.]+))+\))?')
	A = re.compile(r'(?P<key>\w+)=(?P<value>(([\'"]).*?\4)|[0-9.]+)')

	def __add__(self, converter) :
		self.__list__.append(converter)

	@staticmethod
	def addConverter(name, converter) :
		Converter.__converter__[name] = converter

	@staticmethod
	def getConverer(text) :
		if text is None :
			return None

		if Converter.__converter__.get(text) is None :
			module, conName = ut.getdinfo(text)

			mod = importlib.import_module(module)
			return getattr(mod, conName)
		else :
			return Converter.__converter__[text]

	TYPE = re.compile(r'([\'"])(?P<value>.*)\1')
	FLOAT = re.compile(r'\d+.\d*?')

	@staticmethod
	def getValue(value) :
		m = Converter.TYPE.match(value)
		if not m is None :
			return m.group("value")

		m = Converter.FLOAT.match(value)
		if not m is None :
			return float(value)

		return int(value)


	def __init__(self, text):
		self.__list__ = []

		if not text is None :
			self.__initConverter__(text)

	def __initConverter__(self, text):
		self.text: str = text
		cntList = Converter.C.finditer(text)
		for cnt in cntList:
			name = cnt.group("name")
			args = cnt.group("args")
			if args is None:
				self.__add__(self.getConverer(name))
			else:
				f = self.getConverer(name)
				argsList = Converter.A.finditer(args)
				ka = {}
				for a in argsList:
					key = a.group("key")
					value = Converter.getValue(a.group("value"))

					ka[key] = value

				self.__add__(f(**ka))

	def convert(self, text, r) :
		t = text
		for c in self.__list__ :
			t = c(t,r)
			# t, isContinue = c(t, r)
			# isContinue = True if isContinue is None else isContinue
			# if isContinue is False :
			# 	break

		return t
