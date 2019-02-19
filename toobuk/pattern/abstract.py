from abc import *
import re


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
		self.__parent__ = parent
		self.__pattern__ = ptnEle
		self.__type__ = parent.getParent().getJson()['type']

		t = ptnEle.get('type')
		if not ptnEle.get('regx') is None :
			regx = re.compile(ptnEle['regx']['pattern'])
			replace = ptnEle['regx']['replace']

			if t is None :
				self.toConvert = lambda text : regx.sub( replace, text )
			else :
				self.toConvert = lambda text : TYPE_SWITCHER[t]( regx.sub( replace, text ) )
		else :
			if t is None :
				self.toConvert = lambda text : text
			else :
				self.toConvert = lambda text : TYPE_SWITCHER[t]( text )

	def _addData_(self, r, select) :
		r[self.__pattern__['name']] = self.toConvert(select.text)

	@abstractmethod
	def apply( self, source, result ) :
		pass