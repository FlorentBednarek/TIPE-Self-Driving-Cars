from classes import Car
import random, typing
from math import exp

def sig(n: float):
    return (1/(1+exp(n)))


class Network:

    def __init__(self, car: Car):
        self.I_layer = [Neuron(0) for _ in range(8)]
        self.layer_2 = [Neuron(0) for _ in range(4)]
        self.layer_3 = [Neuron(0) for _ in range(4)]
        self.layer_4 = [Neuron(0) for _ in range(2)]
        self.O_layer = [Neuron(0)]
        self.car = car

    def update(self):
        self.I_layer = [Neuron(x) for x in self.car.distances]
        for neuron in self.layer_2:
            neuron.update_value(self.I_layer)
        for neuron in self.layer_3:
            neuron.update_value(self.layer_2)
        for neuron in self.layer_4:
            neuron.update_value(self.layer_3)
        for neuron in self.O_layer:
            neuron.update_value(self.layer_4)
        print(self.O_layer)

    @property
    def left(self):
        return self.O_layer[0].value < 0
    @property
    def right(self):
        return self.O_layer[0].value > 0


class Neuron:

    def __init__(self, value):
        self.value = value
        self.weight = random.random()*2 -1
        self.bias = random.random()

    def normalize(self):
        self.value =  sig(self.value)

    def update_value(self, neurons: typing.List['Neuron']):
        self.value = self.bias + sum([x.value*x.weight for x in neurons])
        self.normalize()

    def __str__(self):
        return str((self.value, self.weight, self.bias))

    def __repr__(self):
        return str(self.value)


# n = Neuron(2)
# print(n.value)
# n.normalize()
# print(n.value)
