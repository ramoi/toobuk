from toobuk.pattern.abstract import *

class Pattern(AbstractPattern) :
	def _getResult_(self) :
		return {}

	def _makeUp_ (self, pattern) :
		for p in pattern :
			self._patternList_.append( PatternElement( p, self ) )


class PatternElement(AbstractPatternElement) :

	def apply(self, source, result) :
		selectList = source.select( self._pattern_.get('selector') )
		self._addData_(result, selectList[0])


