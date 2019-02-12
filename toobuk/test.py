from Crawler import Crawler

c = Crawler()
bs = c.connect('https://www.python.org/about/')
print(bs.head.title)

for meta in bs.head.find_all('meta') :
	print(meta.get('content'))

print (bs.head.find("meta", {"name":"description"}))
print (bs.head.find("meta", {"name":"description"}).get('content'))


for link in bs.find_all('a'):
    print(link.text.strip(), link.get('href'))