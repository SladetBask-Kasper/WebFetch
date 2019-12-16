import requests

class Fetch:
	def __init__(self, url):
		self.url = url
		r = requests.get(url)
		self.html = str(r.text)
		r.close()

	def getAfter(self, searchWord, by):
		return str(self.html.split(searchWord, 1)[1])[:by]
		
	def getHtml(self):
		return self.html
	def getUrl(self):
		return self.url
	def replace(self, all_, with_):
		self.html = self.html.replace(all_, with_)
	def purge(self, these):
		self.html = self.html.replace(these, "")
	def reverse(self):
		self.html = self.html[::-1]

###
### Fetch Webpage (at) Index
###
def fwi(url, searchFor, i):

	r = requests.get(url)
	webpage = str(r.text)
	r.close()
	del r
	result = str(webpage.split(searchFor, 1)[1])[:i]
	return result