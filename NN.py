from classes import *
import random
from math import *

def sig(n):
	return (1/(1+exp(n)))


class neurone(object):
	def __init__(self, value):
		super(neurone, self).__init__()
		self.value = value
		self.weight = random.random()*2 -1
	def normalize(self):
		self.value =  sig(self.value)



n = neurone(2)
print(n.value)
n.normalize()
print(n.value)