from pattern.en import parse, tag, pprint
import string
from random import randint
from lxml import html
import requests


"""I want the data structure to link all the manys verys
muchs suchs mosts etc. groups and then also link all of
the ones with the same word ie much dog very dog many dog"""
class Dogeifier:
	non_plur = ['Many','Such','Most','Very']
	plur = ['Much', 'Very', ]
	verb = ['Many','Much','Such','So','Very', 'Most']
	adj = ['Such','Much']
	doge_particles = []
	s_verbs = []
	s_nouns = []
	s_plurs = []
	s_adjs = []

	def __init__(self, sentence):
		self.sentence = sentence
		self.populate()

	def populate(self):
		parse = self.parse()
		for x in parse.split():
			for y in x:
				if 'NNS' in y[1]:
					self.s_plurs.append(y)
				if 'NN' in y[1]:
					self.s_nouns.append(y)
				elif 'JJ' in y[1]:
					self.s_adjs.append(y)
				elif 'VB' in y[1]:
					self.s_verbs.append(y)
					
		for v in self.s_verbs:
			if v[1] == 'be':
				self.s_verbs.remove(v)

		for adj in self.s_adjs:
			URL = 'http://wordnetweb.princeton.edu/perl/webwn?s=' + adj[0] + '&sub=Search+WordNet&c=0'
			page = html.fromstring(requests.get(URL).text)
			root = page.xpath('/html/body/div[2]/ul[1]/li[1]/b/text()')
			if root:
				print root
				adj[0] = root[0]
			else:
				root = page.xpath('/html/body/div[2]/ul/li[1]/b/text()')
				if not root:
					root = page.xpath('/html/body/div[2]/ul[2]/li[1]/b/text()')
				adj[0] = root[0]

	def parse(self):
		sentence_parse = parse(self.sentence.translate(None, string.punctuation), chunks = False, Lemmata = True)
		return sentence_parse

	def dogeify(self):
		doge_translation = ''
		if not self.doge_particles:
			if self.s_plurs:
				for n in self.s_plurs:
					self.doge_particles.append(self.plur[0] + ' ' + n[0] + '.')

			if self.s_adjs:
				for a in self.s_adjs:
					for x in range(len(self.adj)):
						self.doge_particles.append(self.adj[x] + ' ' + a[0] + '.')

			if self.s_verbs:
				for v in self.s_verbs:
					for x in range(len(self.verb)):
						self.doge_particles.append(self.verb[x] + ' ' + v[0] + '.')

			if self.s_nouns:
				for n in self.s_nouns:
					for x in range(len(self.non_plur)):
						self.doge_particles.append(self.non_plur[x] + ' ' + n[0] + '.')

		if len(self.doge_particles) <= 0:
			return ['Error no particles generated.']

		return self.doge_particles

	def prints(self):
		print self.sentence
		print self.s_nouns

if __name__ == '__main__':
	DM = Dogeifier('I ate chewy pancakes for breakfast today mice.')
	print DM.dogeify()
	"""translation = doge('')"""
	print 'hello'
