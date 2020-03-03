from NN import *
from classes import *
import random


def Shuffle(n1,n2):
    for j,neuron in enumerate(n1.I_layer):
    	i = random.random()
    	if i <0.5:
    		neuron.weight = random.random() * 2 - 1
    	else :
    		neuron = n2.I_layer[j]
    for j,neuron in enumerate(n1.layer_2):

    	i = random.random()
    	if i <0.5:
    		neuron.weight = random.random() * 2 - 1
    	else :
    		neuron = n2.layer_2[j]
    for j,neuron in enumerate(n1.layer_3):

    	i = random.random()
    	if i <0.5:
    		neuron.weight = random.random() * 2 - 1
    	else :
    		neuron = n2.layer_3[j]
    for j,neuron in enumerate(n1.layer_4):

    	i = random.random()
    	if i <0.5:
    		neuron.weight = random.random() * 2 - 1
    	else :
    		neuron = n2.layer_4[j]    
    for j,neuron in enumerate(n1.O_layer):

    	i = random.random()
    	if i <0.5:
    		neuron.weight = random.random() * 2 - 1
    	else :
    		neuron = n2.O_layer[j]
    return n1

def darwin(networks):
	#first 6 stay
	#7-8 become half new half first 2
	#9-10 become new
	mutation_rate = 0.3
	rank = {net : net.score for net in networks}
	rank = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}
	rank2 = []
	for k,v in enumerate(rank):
		rank2.append(v)
	rank2[0] = Network(rank2[0].car)
	rank2[1] = Network(rank2[1].car)
	rank2[2] = Shuffle(rank2[2],rank2[9])
	rank2[3] = Shuffle(rank2[3],rank2[9])

	for net in rank2[4:-2] :
		for neuron in net.I_layer :
			if random.random() <mutation_rate :
				neuron.weight = random.random() * 2 - 1
		for neuron in net.layer_2 :
			if random.random() <mutation_rate :
				neuron.weight = random.random() * 2 - 1
		for neuron in net.layer_3 :
			if random.random() <mutation_rate :
				neuron.weight = random.random() * 2 - 1		
		for neuron in net.layer_4 :
			if random.random() <mutation_rate :
				neuron.weight = random.random() * 2 - 1
		for neuron in net.O_layer :
			if random.random() <mutation_rate :
				neuron.weight = random.random() * 2 - 1
	return rank2
	