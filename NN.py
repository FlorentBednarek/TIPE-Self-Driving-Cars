from classes import *
import random, typing
from math import *

def sig(n):
	return (1/(1+exp(n)))

class Network():
		"""docstring for ClassName"""

		def __init__(self, arg):
			self.I_layer = [0]*8
			self.layer_2 = [0]*4
			self.layer_3 = [0]*4
			self.layer_4 = [0]*2
			self.O_layer = [0]

		def update(self,car):
            if car.distance == self.I_layer:
                return
			self.I_layer = car.distance
            for neuron in self.layer_2:
                neuron.update_value(I_layer)
            for neuron in self.layer_3:
                neuron.update_value(layer_2)
            for neuron in self.layer_4:
                neuron.update_value(layer_3)
            for neuron in self.O_layer:
                neuron.update_value(layer_4)


class Neuron():

	def __init__(self, value):
		self.value = value
		self.weight = random.random()*2 -1

	def normalize(self):
		self.value =  sig(self.value)

    def update_value(neurons: typing.List[Neuron]):
		pass


n = neurone(2)
print(n.value)
n.normalize()
print(n.value)
