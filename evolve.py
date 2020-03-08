from NN import *
from classes import *
import random

'''
def Shuffle(n1,n2):
    for j,neuron in enumerate(n1.I_layer):
        for k,w in enumerate(neuron.weight):
            i = random.random()
            if i <0.5:
                weight = random.random()*2-1
            else :
                w = n2.I_layer[j].weight[k]
    for j,neuron in enumerate(n1.layer_2):
        for w in neuron.weight:

            i = random.random()
            if i <0.5:
                weight = random.random()*2-1
            else :
                w = n2.I_layer[j].weight[k]
    for j,neuron in enumerate(n1.layer_3):
        for w in neuron.weight:
            i = random.random()
            if i <0.5:
                weight = random.random()*2-1
            else :
                w = n2.I_layer[j].weight[k]
    for j,neuron in enumerate(n1.layer_4):
        for w in neuron.weight:
            i = random.random()
            if i <0.5:
                weight = random.random()*2-1
            else :
                w = n2.I_layer[j].weight[k]
    for j,neuron in enumerate(n1.O_layer):
        for w in neuron.weight:
            i = random.random()
            if i <0.5:
                weight = random.random()*2-1
            else :
                w = n2.I_layer[j].weight[k]
    return n1

def darwin(networks):
    #first 6 stay
    #7-8 become half new half first 2
    #9-10 become new
    mutation_rate = 0.3
    # rank = {net : net.score for net in networks}
    # rank = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}
    rank = {net: net.score for net in sorted(networks, key=lambda item: item.score)}
    print(rank)
    rank2 = []
    for k,v in enumerate(rank):
        rank2.append(v)
    rank2[0] = Network(rank2[0].car)
    rank2[1] = Network(rank2[1].car)
    rank2[2] = Shuffle(rank2[2],rank2[9])
    rank2[3] = Shuffle(rank2[3],rank2[9])

    for net in rank2[4:] :
        for neuron in net.I_layer :
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2 -1
        for neuron in net.layer_2 :
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2 -1
        for neuron in net.layer_3 :
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2 -1
        for neuron in net.layer_4 :
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2 -1
        for neuron in net.O_layer :
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2 -1
    return rank2
'''


def mutation(networks):
    mutation_rate = 0.3
    for net in networks :
        for neuron in net.I_layer :
            if random.random() < mutation_rate:
                  neuron.bias = random.random()*2-1
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2-1
        for neuron in net.layer_2 :
            if random.random() < mutation_rate:
                  neuron.bias = random.random()*2-1
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2-1
        for neuron in net.layer_3 :
            if random.random() < mutation_rate:
                  neuron.bias = random.random()*2-1
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2-1        
        for neuron in net.layer_4 :
            if random.random() < mutation_rate:
                  neuron.bias = random.random()*2-1
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2-1
        for neuron in net.O_layer :
            if random.random() < mutation_rate:
                  neuron.bias = random.random()*2-1
            for w in neuron.weight:
                if random.random() <mutation_rate :
                    w = random.random() *2-1
          
    return networks

def swap(n1,n2):
    swap_rate = 0.6
    for i,neuron in enumerate(n1.I_layer) :
        if random.random() < swap_rate:
                  t = neuron.bias
                  neuron.bias = n2.I_layer[i].bias
                  n2.I_layer[i].bias = t
        for j,w in enumerate(neuron.weight):
            if random.random() < swap_rate:
                  t = neuron.bias
                  neuron.bias = n2.I_layer[i].bias
                  n2.I_layer[i].bias = t
    for i,neuron in enumerate(n1.layer_2) :
        if random.random() < swap_rate:
                  t = neuron.bias
                  neuron.bias = n2.layer_2[i].bias
                  n2.layer_2[i].bias = t
        for j,w in enumerate(neuron.weight):
            if random.random() <swap_rate :
                t = w
                w = n2.layer_2[i].weight[j]
                n2.layer_2[i].weight[j] = t
    for i,neuron in enumerate(n1.layer_3) :
        if random.random() < swap_rate:
                  t = neuron.bias
                  neuron.bias = n2.layer_3[i].bias
                  n2.layer_3[i].bias = t
        for j,w in enumerate(neuron.weight):
            if random.random() <swap_rate :
                t = w
                w = n2.layer_3[i].weight[j]
                n2.layer_3[i].weight[j] = t
    for i,neuron in enumerate(n1.layer_4) :
        if random.random() < swap_rate:
                  t = neuron.bias
                  neuron.bias = n2.layer_4[i].bias
                  n2.layer_4[i].bias = t
        for j,w in enumerate(neuron.weight):
            if random.random() <swap_rate :
                t = w
                w = n2.layer_4[i].weight[j]
                n2.layer_4[i].weight[j] = t
    for i,neuron in enumerate(n1.O_layer) :
        if random.random() < swap_rate:
                  t = neuron.bias
                  neuron.bias = n2.O_layer[i].bias
                  n2.O_layer[i].bias = t
        for j,w in enumerate(neuron.weight):
            if random.random() <swap_rate :
                t = w
                w = n2.O_layer[i].weight[j]
                n2.O_layer[i].weight[j] = t
    return (n1,n2)

def darwin(networks):
    rank = {net : net.score for net in networks}
    rank = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}
    rank2 = []

    for k,v in enumerate(rank):
        rank2.append(v)
    new_gen = rank2[-4:]
    for i in range(8):
        r = random.sample(range(0, 3), 2)
        n = swap(new_gen[r[0]],new_gen[r[1]])
        new_gen.append(n[0])
        new_gen.append(n[1])

    
    new_gen = mutation(new_gen)
    return new_gen

