import json, os, re
import codecs
from toobuk.connector_v1 import GetConnector, PostConnector
from toobuk.pattern.list import Pattern as ListPattern
from toobuk.pattern.single import Pattern as SinglePattern
from toobuk.tlogger import TLoggerFactory
import toobuk.util as ut

logger = TLoggerFactory.getLogger()


def copyDict( dic ) :
	return dict(list(dic.items())) if not dic is None else None

class ConfigureError(Exception) :
	def __init__(self, msg) :
		super().__init__(msg)

class Configure :
	__list__ = {}

	@classmethod
	def init(cls) :
		cls.__list__ = {}

	@classmethod
	def get(cls, path) :
		path = str(path) + ".json"

		if cls.__list__.get(path) is None :
			logger.debug('path initialize, path==>{}'.format(path))
			c = Configure(path)
			cls.__list__[path] = c
			return c
		else :
			logger.debug('path exists {}'.format(path))
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
			# jsonTuple = json.loads( f.read(), encoding="utf-8" )
			jsonTuple = json.loads( f.read() )

		return jsonTuple

	def getJson(self) : 
		return self.__json__

	def getConnectManager(self, name) :
		return self.__conf__[name]['connectManager']

class ConnetManager :

	__connector__ = {}
	__connector__['get'] = GetConnector
	__connector__['post'] = PostConnector

	@staticmethod
	def addConnector(name, connector) :
		logger.debug('add connector => name={} connector={}'.format(name, connector.__name__) )
		ConnetManager.__connector__[name] = connector

	def __init__(self, json) :
		self.__json__ = json

		##parameter 설정
		self.__parameter__ = self.__makeParameter__(json.get('parameter'), json.get('for') )
		self.__connector__ = self.__makeConnector__( )

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
				raise ConfigureError('Not support number for loop')

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

	def __makeConnector__(self) :
		conType = self.__json__.get('conn.type') or 'get'

		if ConnetManager.__connector__.get(conType) is None :
			return ut.runPlugin(conType, self.__json__)
		else :
			return ConnetManager.__connector__[conType](self.__json__)

	def getParameter(self) :
		return self.__parameter__

	def getRealParameter(self, parameter, looopJson) :
		return self.__parameter__ if(parameter, looopJson) == (None, None) else self.__makeParameter__(parameter, looopJson)


	def getConnector( self ) :
		# looopJson = self.__json__.get('for') if looopJson is None else looopJson
		# param = self.__parameter__ if parameter is None else self.__makeParameter__(parameter, looopJson)
		return self.__connector__

	def getOutput(self) :
		return self.__output__

	def get(self, outputPath, parameter=None, headers=None, looopJson=None) :
		connector = self.getConnector()
		output = self.getOutput()

		paramList:[] = self.getRealParameter(parameter, looopJson)

		result = DataSet()

		for param in paramList :
			r = connector.get(headers, param)
			output.apply(self, r['source'], result, r['parameter'], outputPath)

		return result.getDataSet()

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
		return self.__json__

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
		outType = self.__json__.get('type') or "single"

		if outType == 'list' :
			self._p_ = ListPattern(self.__json__['pattern'], self)
		else :
			self._p_ = SinglePattern(self.__json__['pattern'], self)

	def apply(self, toobuk, source, result, parameter) :
		resultData = self._p_.apply(source)
		result.add(self.__eleKey__, resultData, parameter)

	def getParent(self) :
		return self.__parent__

	def getJson(self) :
		return self.__json__

class DataSet :
	def __init__(self) :
		self.__result__ = {}

	def getDataSet(self) :
		return self.__result__

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

	@staticmethod
	def replace(url, *rl):
		if (None, None) == rl:
			return url

		for r in rl:
			if not r:
				continue

			for key in r.keys():
				url = url.replace('#' + str(key) + '#', r[key])

		return url

	def replaceUrl(self, url) :
		return Parameter.replace( url, self.__param__, self.__looop__  )

	def getData(self) :
		data = {}
		for r in [self.__param__, self.__looop__]:
			if not r:
				continue

			for key in r.keys():
				data[key] = r[key]

		return data

	def isEmpty(self) :
		return not bool( self.__param__ or self.__looop__ )

	def isEmptyParameter(self) :
		return not bool(self.__param__)

	def isContainedParameter(self, json) :
		return self.__param__.items() < json.items()