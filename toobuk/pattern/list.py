from toobuk.pattern.abstract import *

class Pattern(AbstractPattern) :
	def _getResult_(self) :
		return []

	def _makeUp_ (self, pattern) :
		for p in pattern :
			self._patternList_.append( PatternElement( p, self ) )


class PatternElement(AbstractPatternElement) :

	def apply( self, source, result ) :
		selectList = source.select( self.__pattern__.get('selector') )

		if not self.__pattern__.get('slice') is None :
			start = self.__pattern__['slice']['start'] if self.__pattern__['slice'].get('start') is not None else 0
			end = self.__pattern__['slice']['end'] if self.__pattern__['slice'].get('end') is not None else len(selectList)
			selectList = selectList[start:end]

		for index, select in enumerate(selectList) :
			if len(result) < index + 1:
				result.append({})

			self._addData_( result[index], select) 