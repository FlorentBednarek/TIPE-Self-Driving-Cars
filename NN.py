from classes import Car
import random, typing
from math import exp

def sig(n: float):
    return (1/(1+exp(n)))


class Network:

    def __init__(self, car: Car):
        self.I_layer = [0]*8
        self.layer_2 = [0]*4
        self.layer_3 = [0]*4
        self.layer_4 = [0]*2
        self.O_layer = [0]
        self.car = car

    def update(self):
        if self.car.distance == self.I_layer:
            return
        self.I_layer = self.car.distance
        for neuron in self.layer_2:
            neuron.update_value(I_layer)
        for neuron in self.layer_3:
            neuron.update_value(layer_2)
        for neuron in self.layer_4:
            neuron.update_value(layer_3)
        for neuron in self.O_layer:
            neuron.update_value(layer_4)


class Neuron:

    def __init__(self, value):
        self.value = value
        self.weight = random.random()*2 -1
        self.bias = random.random()

    def normalize(self):
        self.value =  sig(self.value)

    def update_value(neurons: typing.List['Neuron']):
        self.value = self.bias + sum([x.value*x.weight for x in neurons])
        self.normalize()


# n = Neuron(2)
# print(n.value)
# n.normalize()
# print(n.value)
