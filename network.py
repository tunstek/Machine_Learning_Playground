
import graphviz as gv
import sys, random

from layer import *
from neuron import *
from synapse import *

from functions import *



MAX_INT = sys.maxint



class Network:

    def __init__(self, number_of_inputs, number_of_outputs):

        self.neuron_count = 0
        self.hidden_layer_count = 0

        self.layers = {} # a dict of layers keyed by their ids


        # Create the input and output layers
        input_neurons = []
        for i in range(0, number_of_inputs):
            temp = Neuron(self.neuron_count)
            input_neurons.append(temp)
            self.neuron_count += 1
        output_neurons = []
        for i in range(0, number_of_outputs):
            temp = Neuron(self.neuron_count)
            output_neurons.append(temp)
            self.neuron_count += 1
        self.layers[0] = Layer(0,input_neurons, "blue")
        self.layers[MAX_INT] = Layer(MAX_INT, output_neurons, "red")

    def __str__(self):
        ret = "Network:\n"
        for key in self.layers:
            ret = ret + str(self.layers[key]) + "\n\n"
        return ret


    def add_layer(self):
        # create a new neuron for the layer
        new_neuron = Neuron(self.neuron_count)
        self.neuron_count += 1

        # simplify all connections
        # all neurons in previous layer
        for neuron in self.layers[self.hidden_layer_count].neurons:
            #randomly select a forward synapse
            rand_synapse = neuron.get_rand_forward_synapse()
            if rand_synapse is not None:
                #remove all other synapses
                for synapse in neuron.synapses:
                    if synapse != rand_synapse:
                        neuron.remove_connection(neuron, synapse.to)

                temp_to = synapse.to
                synapse.to = new_neuron
                new_neuron.add_connection(temp_to, 1) # give the new connection a weight of 1


        #REPLACE_ALL_CONNECTIONS = True

        #if REPLACE_ALL_CONNECTIONS:
        #    for neuron in self.layers[self.hidden_layer_count]
        #        #randomly select a forward synapse
        #        synapse = neuron.get_rand_forward_synapse()
        #        temp_to = synapse.to
        #        synapse.to = new_neuron
        #        new_neuron.add_connection(temp_to, 1) # give the new connection a weight of 1

            # get all previous layer neuron forward connections and connect them to this neuron
            #synapses = self.layers[self.hidden_layer_count].get_all_forward_synapses()
            # keep track of new connnections to avoid duplicates
            #conn_frm = []
            #for synapse in synapses:
            #    if synapse.frm.id not in conn_frm:
            #        temp_to = synapse.to
            #        synapse.to = new_neuron
            #        new_neuron.add_connection(temp_to, synapse.weight)
            #        conn_frm.append(synapse.frm.id)


        self.hidden_layer_count += 1
        new_layer = Layer(self.hidden_layer_count, [new_neuron], generate_color())
        self.layers[self.hidden_layer_count] = new_layer



    def layers_fully_interconnected(self, layerA, layerB):
        for neuronA in layerA.neurons:
            for neuronB in layerB.neurons:
                if neuronB not in neuronA.synapses:
                    return False
        return True

    def get_layers_with_available_connections(self):
        # assumes layers are added chronalogically
        ret = []
        for index in range(0, self.hidden_layer_count+1):
            temp_layerA = self.layers[index]
            if index == self.hidden_layer_count:
                #check this index layer against the outputs
                temp_layerB = self.layers[MAX_INT]
            else:
                temp_layerB = self.layers[index+1]
            if not self.layers_fully_interconnected(temp_layerA, temp_layerB):
                ret.append((temp_layerA,temp_layerB))
        return ret

    def add_rand_interlayer_connection(self):

        # ADDING CONNECTIONS THAT ALREADY EXIST

        # select a set of layers with available connections
        available_connections = self.get_layers_with_available_connections()

        if len(available_connections) == 0:
            print "add_rand_interlayer_connection: Network is fully interconnected, cannot add node"
        else:
            selected_layers = random.randint(0,len(available_connections)-1)

            layerA = available_connections[selected_layers][0]
            layerB = available_connections[selected_layers][1]

            # select a random neuron from each layer
            neuronA = layerA.get_rand_neuron()
            neuronB = layerB.get_rand_neuron()

            while neuronB in neuronA.synapses or neuronA in neuronB.synapses:
                # select another pair of neurons
                neuronA = layerA.get_rand_neuron()
                neuronB = layerB.get_rand_neuron()

            if neuronA.add_connection(neuronB, random.uniform(0,1)):
                print "connected " + neuronA.id + " to " + neuronB.id
            else:
                print "Connections not added: " + neuronA.id + " to " + neuronB.id





    def visualise(self, randomEdgeColors=None):

        # build the visual graph here
        vis = gv.Digraph(comment='Graph') # a visual representation of the graph
        #vis.graph_attr.update(newrank='true')
        vis.graph_attr.update(rankdir='LR')
        vis.graph_attr.update(splines='line')

        vis.graph_attr.update(size="2000,2000",pad="2", nodesep="3", ranksep="4")


        if randomEdgeColors is None:
            vis.attr('edge', color="black")
        else:
            vis.attr('edge', color=generate_color())


        for key in self.layers:
            for node in self.layers[key].neurons:
                temp = gv.Digraph(name='cluster_'+str(key))

                temp.graph_attr.update(rankdir='LR')

                if key == 0:
                    temp.graph_attr.update(rank='min')
                    temp.graph_attr.update(label='Inputs')
                elif key == MAX_INT:
                    temp.graph_attr.update(label='Outputs')
                    temp.graph_attr.update(rank='max')
                else:
                    temp.graph_attr.update(label='cluster_'+str(key))
                    temp.graph_attr.update(rank=str(key))

                temp.node(node.id, color=self.layers[key].color)
                vis.subgraph(temp)

        # make all the connections
        for key in self.layers:
            for nodeA in self.layers[key].neurons:
                for connection in nodeA.get_forward_synapses():
                    vis.edge(nodeA.id, connection.to.id)

        vis.render('img/g1.gv', view=True)



if __name__ == "__main__":

    network = Network(3,3)
    network.add_rand_interlayer_connection()
    network.add_rand_interlayer_connection()

    network.add_layer()

    print network
    print "\n\n"

    network.add_rand_interlayer_connection()

    print network


    network.visualise()
