from abc import *
import json, os, re
from urllib.request import urlopen
import codecs
from bs4 import BeautifulSoup

from toobuk.pattern.list import Pattern as ListPattern
from toobuk.pattern.single import Pattern as SinglePattern

def replace(str, *rl) :
	if (None, None) == rl : 
		return str

	for r in rl :
		if not r : 
			continue

		for key in r.keys() :
			str = str.replace('#'+key+'#', r[key])

	return str

def copyDict( dic ) :
	return dict(list(dic.items())) if not dic is None else None

class ConfigureError(Exception) :
	pass

class Configure :
	__list__ = {}

	@classmethod
	def get(cls, path) :
		path = path + ".json"

		if cls.__list__.get(path) is None :
			c = Configure(path)
			cls.__list__[path] = c
			return c
		else :
			return cls.__list__[path]

	def __init__(self, path) :
		self.__json__ = self.__load__(path)

		self.__conf__ = {}
		for key in self.__json__.keys() :
			self.__conf__[key] = {}
			self.__conf__[key]['connectManager'] = ConnetManager(self.__json__[key]) 

	def __load__(self, path) :
		jsonTuple = None
		with codecs.open( path, 'r', encoding='utf-8' ) as f : 
			jsonTuple = json.loads( f.read(), encoding="utf-8" )

		return jsonTuple

	def getJson(self) : 
		return self.__json__

	def getConnectManager(self, name) :
		return self.__conf__[name]['connectManager']

class ConnetManager : 
	def __init__(self, json) :
		self.__json__ = json

		##parameter 설정
		self.__parameter__ = self.__makeParameter__(json.get('parameter'), json.get('for') )

		##output 설정
		self.__output__ = Output(json['output'])

	def __makeParameter__(self, parameter, looopJson) :
		parameter = parameter if not isinstance( parameter, dict ) else [parameter]
		looop = None
		if not looopJson is None :
			if looopJson['type'] == 'number' :
				start = looopJson['start']
				end = looopJson['end'] + 1
				step = looopJson['step'] if 'step' in looopJson is not None else 1

				looop = [ { looopJson['name'] : str(pf) } for pf in range( start, end, step ) ]
			else :
				raise ConfigureError

		if ( parameter, looop) == ( None, None ) :
			return [ Parameter()]
		elif parameter is None and not looop is None :
			return [ Parameter( None, lp ) for lp in looop ]
		elif not parameter is None and looop is None :
			return [ Parameter( param, None ) for param in parameter ]
		else :
			p = []
			for pEle in parameter :
				for lEle in looop :
					# p.append( { **pEle, **lEle } )
					p.append( Parameter( pEle, lEle) )
			return p

	def getConnector( self, parameter, looopJson ) :
		if ( None, None ) == ( parameter, looopJson ) :
			return Connector(self.__parameter__, self.__json__ )

		looopJson = self.__json__.get('for') if looopJson is None else looopJson 
		param = self.__parameter__ if parameter is None else self.__makeParameter__(parameter, looopJson)

		return Connector( param, self.__json__ )

	def getOutput(self) :
		return self.__output__


class Connector :
	def __init__( self,  parameter, json ) :
		self.__parameter__ = parameter
		self.__json__ = json
		self.__idx__ = 0

	def isFirst( self ) :
		return self.__idx__ == 0

	def hasMoreConnect(self) :
		return self.__idx__ < len(self.__parameter__) 

	def connect(self) :
		parameter = self.__parameter__[self.__idx__] 

		url =  parameter.replaceUrl(self.__json__['url'])
		html = urlopen( url )
		bs = BeautifulSoup(html, self.__json__['bs.type'], from_encoding='utf-8' if self.__json__.get('encoding') is None else self.__json__['encoding'] )
		self.__idx__ = self.__idx__ + 1

		return { 'source' : bs, 'parameter' : parameter } 

class Output : 
	def __init__(self, oj) :
		self.__json__ = oj
		self._oe_ = {}
		self._makeUp_(oj)

	def _makeUp_(self, oj) :
		#json의 output
		for key in oj.keys() :
			#output 각각의 key
			self._oe_[key] = OutputElement(key, oj[key], self)

	def getJson(self) :
		return __json__

	def apply(self, toobuk, source, result, parameter, target) :
		for oe in self._oe_ if not target else target :
			self._oe_[oe].apply(toobuk, source, result, parameter)

class OutputElement :
	def __init__(self, eleKey, oEle, parent) :
		self.__parent__ = parent
		self.__eleKey__ = eleKey
		self.__json__ = oEle
		self._p_ = None

		self._makeUp_()

	def _makeUp_( self ) :
		if self.__json__['type'] == 'list' :
			self._p_ = ListPattern(self.__json__['pattern'], self)
		else :
			self._p_ = SinglePattern(self.__json__['pattern'], self)

	def apply(self, toobuk, source, result, parameter) :
		resultData = self._p_.apply(source)
		result.add(self.__eleKey__, resultData, parameter)

		# if 'join' in self.__json__ :
		# 	path = self.__json__['join']['ref']
		# 	joinResult = toobuk.get(self.__json__['join']['ref'], [ parameter.getOnlyParameter() ] )

		# 	pathInfo = toobuk.getPathInfo(path)
		# 	print( joinResult[pathInfo.group('output')] )
		# 	print( joinResult )
		# 	joinData = joinResult[pathInfo.group('output')]['data'] if self.__json__['join']['ref'] == 'list' else joinResult[pathInfo.group('output')][0]['data']
		# 	result.join( self.__eleKey__, self.__json__['join'], joinData, parameter )
			

	def getParent(self) :
		return self.__parent__

	def getJson(self) :
		return self.__json__

class DataSet :
	def __init__(self) :
		self.__result__ = {}

	def getDataSet(self) :
		return self.__result__

	# def joinData( self, joinJson, result, joinData, parameter ) :
	# 	if isinstance(joinData, dict) :
	# 		if isinstance(result, dict) :
	# 			result.update(joinData)
	# 		else :
	# 			joinData['data'] = result 
	# 			result = joinData
	# 	else :
	# 		if isinstance(result, dict) :
	# 			result['data'] = joinData
	# 		else :
	# 			joinKey = joinJson['joinKey']
	# 			for r in result :
	# 				for jr in joinData :
	# 					if r[joinKey[0]] == jr[joinKey[1]] :
	# 						r.update(jr)

	# def join( self, key, joinJson, joinData, parameter ) :
	# 	if not key in self.__result__ :
	# 		return

	# 	if parameter.isEmptyParameter() :
	# 		self.joinData( joinJson, self.__result__[key], joinData, parameter) 
	# 	else :
	# 		rEle = None
	# 		for r in self.__result__[key] :
	# 			if parameter.isContainedParameter(r) :
	# 				rEle = r

	# 		self.joinData( joinJson, rEle, joinData, parameter) 

	def add( self, key, resultData, parameter ) :
		if parameter.isEmptyParameter() :
			self.addForOnlyOne(key, resultData)
		else :
			self.addForMultiParameter(key, resultData, parameter)


	def addForMultiParameter( self, key, resultData, parameter ) :
		if key in self.__result__ :
			isContainParameterResult = False


			if not isinstance(self.__result__[key], list) :
				self.__result__[key] = [ self.__result__[key]  ]

			for r in self.__result__[key] :
				if parameter.isContainedParameter(r) :
					r['data'] = r['data'] + resultData
					isContainParameterResult = True

			if not isContainParameterResult :
				rEle = copyDict( parameter.getOnlyParameter() )
				rEle['data'] = resultData
				self.__result__[key].append( rEle )
		else :
			r = copyDict( parameter.getOnlyParameter() )
			r['data'] = resultData
			self.__result__[key] = r

	def addForOnlyOne( self, key, resultData ) :
		if key in self.__result__ :
			if isinstance(self.__result__[key], dict) :
				self.__result__[key] = [self.__result__[key]]
				self.__result__[key].append(resultData)
			else :
				self.__result__[key] = self.__result__[key] + resultData
		else :
			self.__result__[key]  = resultData


class Parameter :
	def __init__(self, param = None, looop = None) :
		self.__param__ = param
		self.__looop__ = looop

	def getParameter(self) :
		copyDict(self.__param__.items()) + copyDict(self.__looop__.items())

	def getOnlyParameter(self) :
		return self.__param__

	def getLoop(self) :
		return self.__looop__

	def replaceUrl(self, url) :
		return replace( url, self.__param__, self.__looop__  )

	def isEmpty(self) :
		return not bool( self.__param__ or self.__looop__ )

	def isEmptyParameter(self) :
		return not bool(self.__param__)

	def isContainedParameter(self, json) :
		return self.__param__.items() < json.items()

