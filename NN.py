from classes import *
import random
from math import *

def sig(n):
	return (1/(1+exp(n)))

class reseau(object):
		"""docstring for ClassName"""
		def __init__(self, arg):
			super(ClassName, self).__init__()

			self.I_layer = [0]*8
			self.layer_2 = [0]*4
			self.layer_3 = [0]*4
			self.layer_4 = [0]*2
			self.O_layer = [0]
		def uptdate(self,car):
			self.I_layer[i for i in car.distance]



class neurone(object):
	def __init__(self, value):
		super(neurone, self).__init__()
		self.value = value
		self.weight = random.random()*2 -1
	def normalize(self):
		self.value =  sig(self.value)
		def function():
			pass


n = neurone(2)
print(n.value)
n.normalize()
print(n.value)