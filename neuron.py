
from synapse import *

import random

class Neuron:
    def __init__(self, neuron_id):

        self.id = str(neuron_id)
        self.value = 0.0

        self.synapses = []

    def __str__(self):
        return self.id + " connections: " + str([(x.to.id,x.weight) for x in self.synapses])

    def get_synapses_ids(self):
        ret = []
        for synapse in self.synapses:
            ret.append(synapse.to.id)
        return ret

    def add_connection(self, to, weight):
        # check if a connection already exists
        if to.id not in self.get_synapses_ids():
            syn = Synapse(self, to, weight)
            # add a forward connecting synapse to this neuron
            self.synapses.append(syn)
            # add a backward connecting synapse to the other neuron
            to.synapses.append(syn)
            return 1
        return 0

    def remove_connection(self, frm, to):
        # there should only exist one connection between frm and to
        # but we must delete the connection from both sides
        frm.remove_synapse(to)
        to.remove_synapse(frm)
    def remove_synapse(self, node):
        try:
            self.synapses.pop(node)
        except:
            pass

    def get_forward_synapses(self):
        ret = []
        for synapse in self.synapses:
            if synapse.frm == self:
                ret.append(synapse)
        return ret
    def get_backward_synapses(self):
        ret = []
        for synapse in self.synapses:
            if synapse.to == self:
                ret.append(synapse)
        return ret

    def get_rand_forward_synapse(self):
        forward_synapses = self.get_forward_synapses()
        if len(forward_synapses) > 0:
            index = random.randint(0, len(forward_synapses)-1)
            return forward_synapses[index]
        else:
            return None

if __name__ == "__main__":
    neuronA = Neuron(0)
    neuronB = Neuron(1)

    neuronA.add_connection(neuronB, 0.12424)
    print neuronA
