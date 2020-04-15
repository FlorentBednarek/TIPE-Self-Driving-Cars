from classes import Car
import random, typing
from math import exp

def sig(n: float,a=1):
    return (1/(1+exp(-a*n)))


class Network:

    def __init__(self, car: Car):
        self.I_layer = [Neuron(0,4) for _ in range(5)]
        self.layer_2 = [Neuron(0,3) for _ in range(4)]
        self.layer_3 = [Neuron(0,2) for _ in range(3)]
        self.layer_4 = [Neuron(0,0) for _ in range(2)]
        # self.O_layer = [Neuron(0,0)]
        self.score = 0
        self.dead = 0
        self.car = car

    def update(self):
        # self.I_layer = [Neuron(max(x,0)) for x in self.car.distances]
        # self.I_layer = [Neuron(max(0, self.car.raytrace(36*i-70, 40, return_real_distance=False)), 4) for i in range(5)]
        for i,n in enumerate(self.I_layer):
            n.value = max(0, self.car.raytrace(36*i-70, 80, return_real_distance=False))

        #    neuron.normalize()
        for i,neuron in enumerate(self.layer_2):
            neuron.update_value(self.I_layer, i)
        for i,neuron in enumerate(self.layer_3):
            neuron.update_value(self.layer_2, i)
        for i,neuron in enumerate(self.layer_4):
            neuron.update_value(self.layer_3, i)

    @property
    def direction(self):
        return round(self.layer_4[0].value*2-1,3)
    @property
    def engine(self):
        return self.layer_4[1].value 
    
    

class Neuron:

    def __init__(self, value, x):
        self.value = value
        self.weight = [random.random()*4-2 for i in range(x)]
        self.bias = random.random()*2-1

    def normalize(self):
        self.value = sig(self.value, 3)

    def update_value(self, neurons: typing.List['Neuron'], target, a = 1):
        self.value = sum([x.value*x.weight[target] for x in neurons]) + self.bias
        self.normalize()

    def __str__(self):
        return str((self.value, self.weight, self.bias))

    def __repr__(self):
        return str(self.value)


# n = Neuron(2)
# print(n.value)
# n.normalize()
# print(n.value)
