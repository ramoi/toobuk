from toobuk.pattern.abstract import *
import toobuk.util as ut


class Pattern(AbstractPattern):
    def _getResult_(self):
        return []

    def _makeUp_(self, pattern):
        for p in pattern:
            self._patternList_.append(PatternElement(p, self))


class PatternElement(AbstractPatternElement):

	def _makeUp_(self) :
		self.skip = self.__makeSkip__()

	def __makeSkip__(self) :
		if not self._pattern_.get('skip') is None:
			skip = self._pattern_.get('skip')
			skipFunc = ut.getPlugin(skip)

			def skip(selectList) :
				resultList = []
				for select in selectList:
					if not skipFunc(select.text):
						resultList.append(select)

				return resultList

			return skip
		if not self._pattern_.get('skip.value') is None:
			def skip(selectList) :
				resultList = []
				for select in selectList:
					if select.text != self._pattern_['skip.value']:
						resultList.append(select)

				return resultList

			return skip
		elif not self._pattern_.get('slice') is None:
			slice = self._pattern_.get('slice')
			if isinstance(slice, dict):
				slice = [slice]

			def skip(selectList) :
				resultList = []
				for s in slice:
					sp = s.get('start') or 0
					ep = s.get('end') or len(selectList)
					resultList = resultList + selectList[sp:ep]

				return resultList

			return skip
		else :
			return lambda select : select

	def apply(self, source, result):
		selectList = source.select(self._pattern_.get('selector'))
		resultList = self.skip(selectList)

		for index, select in enumerate(resultList):
			if len(result) < index + 1:
				result.append({})

			self._addData_(result[index], select)
