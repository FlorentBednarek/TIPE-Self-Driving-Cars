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
        # self.I_layer = [Neuron(max(x,0)) for x in self.car.distances]
        self.I_layer = [Neuron(max(0, self.car.raytrace(20*i-70, 40, return_real_distance=False))) for i in range(8)]
        print(self.I_layer)
        # for neuron in self.I_layer:
        #     # neuron.normalize()
        #     neuron.value /= 40
        print("après normalisation",self.I_layer)
        for neuron in self.layer_2:
            neuron.update_value(self.I_layer)
        for neuron in self.layer_3:
            neuron.update_value(self.layer_2)
        for neuron in self.layer_4:
            neuron.update_value(self.layer_3)
        for neuron in self.O_layer:
            neuron.update_value(self.layer_4)
        # print("1",self.I_layer,
        # "\n2", self.layer_2,
        # "\n3", self.layer_3,
        # "\n4", self.layer_4,
        # "\nOUTPUT", self.O_layer)

    @property
    def left(self):
        return self.O_layer[0].value < 0.5
    @property
    def right(self):
        return self.O_layer[0].value > 0.5


class Neuron:

    def __init__(self, value):
        self.value = value
        self.weight = random.random()*2 -1
        self.bias = random.random()

    def normalize(self):
        self.value = sig(self.value)

    def update_value(self, neurons: typing.List['Neuron']):
        self.value = round(abs(sum([x.value*x.weight for x in neurons])), 6)
        # self.normalize()

    def __str__(self):
        return str((self.value, self.weight, self.bias))

    def __repr__(self):
        return str(self.value)


# n = Neuron(2)
# print(n.value)
# n.normalize()
# print(n.value)
