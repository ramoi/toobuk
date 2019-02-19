from urllib.request import urlopen
from bs4 import BeautifulSoup

class Connector :

	def connect(self, url, parser='html.parser') :
		print(url)
		html = urlopen(url)
		bs = BeautifulSoup(html, parser)

		return bs

if __name__ == '__main__' :
	c = Connector()
	bs = c.connect('http://www.naver.com')
	print(bs)
