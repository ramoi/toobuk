#from abc import *
from toobuk.conf import Configure, DataSet
import re

class ToobukError(Exception) :
	pass

# class Toobuk(metaclass=ABCMeta) :
class Toobuk :

	def __init__(self, path) :
		self.__conf__ = Configure.get(path)

	@staticmethod
	def __toArray__( s ) :
		return s.split(',') if s else s

	__PATH_REG__ = re.compile(r'^(?P<name>.+?)(/(?P<output>.*))?$')

	@staticmethod
	def getPathInfo(path) :
		return Toobuk.__PATH_REG__.search(path)


	def get(self, path, parameter=None, loo0pJson=None) :
		path = Toobuk.getPathInfo(path)

		connMgr = self.__conf__.getConnectManager(path.group('name'))
		connector = connMgr.getConnector(parameter, loo0pJson)
		output = connMgr.getOutput()

		result = DataSet()

		while connector.hasMoreConnect() :
			r = connector.connect()
			output.apply(self, r['source'], result, r['parameter'], Toobuk.__toArray__(path.group('output')) )

		return result.getDataSet()

	def grumble(self) :
		pass
