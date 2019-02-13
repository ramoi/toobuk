#from abc import *
from toobuk.conn import Connector
from toobuk.conf import Configure
import toobuk.util as util

class ToobukError(Exception) :
	pass

# class Toobuk(metaclass=ABCMeta) :
class Toobuk :

	def __init__(self, path) :
		self._setJson(path)
		self.__connector = Connector()

	def _setJson( self, path ) :
		conf = Configure( path )
		self.__json__ = conf.getJson()

	def grumble(self) :
		pass

	def getJson(self) :
		return self.__json__

	def get(self, jsonName, parameter=None) :
		json = self.__json__[jsonName]
		url = json['url']

		parameter = parameter if parameter is not None else json.get('parameter') if json.get('parameter') is not None else {}
		# if parameter is None :
		# 	raise ToobukError


		if isinstance(parameter.get('data'), list) :
			result = []
			key = parameter['arrayKey']
			for p in parameter['data'] : 
				connUrl = util.replace( url, p )

				data = self.getData(connUrl, json)
				r = { key : p[key], 'data' : data }

				if 'join' in json :
					self.join(r, json, p)

				result.append(r)

			return result
		else :
			connUrl = util.replace( url, parameter )
			result = self.getData(connUrl, json)

			if 'join' in json :
				self.join(result, json, parameter)

			return result

	def join(self, result, json, parameter) :
		joinData = self.get(json['join']['ref'], parameter)

		for jk in json['join']['get'] :
			result[jk] = joinData[0][jk]

	def getData(self, url, json) :
		if 'for' in json :
			result = []


			paramName = None
			start = end = step = 0
			#if json['for']['type'] is 'number' :
			if json['for']['type'] == 'number' :
				paramName = json['for']['name']
				start = json['for']['start']
				end = json['for']['end'] + 1
				step = json['for']['step'] if 'step' in json['for'] is not None else 1

				# print('paramName= %s, start = %s, end= %s, step= %s' % (paramName, start, end, step) )
			else :
				print( json['for']['type'] is 'number' )
				print( json['for']['type'] == 'number' )
				print( type(json['for']['type']) )
				print( json['for']['type'] )

			isSingleApply = False
			for looop in range(start, end, step) :
				looop = str(looop) if isinstance(looop, int) else looop

				loopUrl = util.replace( url, { paramName : looop } )
				if None in ( json['output'].get("single"), json['output'].get("list") ) : 
					result = result + self.gathering(loopUrl, json)
				else :
					#리스는 for문을 도는 동안 모두 가져오고 single도 모두 가져온다.
					if util.toBool(json['output']["single"]["isRepeat"]) :
						result['list'] = result['list'] + self.gathering(loopUrl, json)['list']
						resultData = self.gathering(loopUrl, json)
						result['list'] = result['list'] + resultData['list']
						result['single'] = result['list'] + resultData['list']
					#리스는 for문을 도는 동안 모두 가져오고 single은 한 번만 가져온다.
					else :
						if not isSingleApply :
							resultData = self.gathering(loopUrl, json)
							result['list'] = result['list'] + resultData['list']
							result['single'] = resultData['single']
							isSingleApply = True
						else :
							result['list'] = result['list'] + self.gathering(loopUrl, json, 'LIST')

			return result
		else :
			return self.gathering( url, json )


	def gathering( self, url, json, sep='BOTH' ) :
		source = self.__connector.connect( url, json['bs.type'] )

		if sep in ( 'BOTH', 'LIST' ) :
			rlist = self.applyPattern( source, json['output'].get("list"), True)
		if sep in ( 'BOTH', 'SINGLE' ) :
			rsingle = self.applyPattern( source, json['output'].get("single"), False)

		if None in ( rlist, rsingle ) :
			return rlist if rlist is not None else rsingle
		else :
			return { 'list' :rlist, 'single' : rsingle }

	def applyPattern(self, source, patternList, isList) :
		if patternList is None : 
			return

		result = []
		for pattern in patternList :
			if not pattern.get('selector') is None :
				self.selector(source, pattern, result, isList)
			else :
				raise ToobukError

		return result


	def selector(self, source, pattern, result, isList) :
		resultLen = len(result) - 1
		reg = pattern.get('regx')

		print( pattern.get('selector'))

		selectList = source.select(pattern.get('selector') ) 

		def addData(idx, select) :
			if len(result) < idx + 1:
				result.append({})

			if reg is None :
				result[idx][pattern['name']] = util.toConvert(select.text, pattern.get('type'))
			else :
				result[idx][pattern['name']] = util.toConvert( reg['re'].sub( reg['replace'], select.text ), pattern.get('type') )


		if isList :
			if not pattern.get('slice') is None :
				start = pattern['slice']['start'] if pattern['slice'].get('start') is not None else 0
				end = pattern['slice']['end'] if pattern['slice'].get('end') is not None else len(selectList)
				selectList = selectList[start:end]

			for index, select in enumerate(selectList) :
				addData(index, select)
		else :
			addData(0, selectList[0])


