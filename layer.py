import sys, random

from neuron import *

MAX_INT = sys.maxint



class Layer:

    def __init__(self, layer_id, initial_neurons, color=None):
        if color is None:
            self.color = "black"
        else:
            self.color = color
        self.id = str(layer_id)
        if type(initial_neurons) != list:
            print "Layer: Please give initial_neurons as a List"
            exit()
        else:
            self.neurons = initial_neurons

    def __str__(self):
        if self.id == str(0):
            return "Input Layer: " + "\n" + str([str(x) for x in self.neurons])
        elif self.id == str(MAX_INT):
            return "Output Layer: " + "\n" + str([str(x) for x in self.neurons])
        else:
            return "Layer: " + self.id + "\n" + str([str(x) for x in self.neurons])


    def add_neuron(self, neuron):
        self.neurons.append(neuron)
    def remove_neuron(self, neuron):
        self.neurons.pop(neuron)

    def get_rand_neuron(self):
        neuron_index = random.randint(0, len(self.neurons)-1)
        return self.neurons[neuron_index]

    def get_all_forward_synapses(self):
        ret = []
        for neuron in self.neurons:
            for synapse in neuron.get_forward_synapses():
                ret.append(synapse)
        return ret

if __name__ == "__main__":

    neuronA = Neuron("A")
    neuronB = Neuron("B")
    neuronC = Neuron("C")
    neurons = []
    neurons.append(neuronA)
    neurons.append(neuronB)
    neurons.append(neuronC)

    neuronA.add_connection(neuronB, 0.23342)
    neuronA.add_connection(neuronC, 0.23342)

    layer = Layer(0, neurons)


    print layer
