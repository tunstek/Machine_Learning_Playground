
from clustered_graph import *
from functions import *

import random, sys



DEBUG = True
MAX_INT = sys.maxint


# input layer is always 0
# output layer is always MAX_INT



class Network(Graph):

    # Constructor function
    def __init__(self, numberOfInputNodes, numberOfOutputNodes):

        super(Network, self).__init__()

        self.nodeCount = 0
        self.hiddenLayerCount = 0

        ##populate the network with inputs and outputs
        self.add_layer("blue", 0) # input nodes
        self.add_layer("red", MAX_INT) # output nodes
        for i in range(0, numberOfInputNodes):
            #print "Adding in node"
            self.add_node(self.nodeCount, layer_id=0)
        for j in range(0, numberOfOutputNodes):
            #print "Adding out node"
            self.add_node(self.nodeCount, layer_id=MAX_INT)




    def __str__(self):
        ret = super(Network, self).__str__()
        return ret


    def add_layer(self, nodeColor=None, layer_id=None):
        if layer_id is None:
            self.hiddenLayerCount += 1
            self.add_cluster(self.hiddenLayerCount, nodeColor)

            self.add_node(self.nodeCount, layer_id=self.hiddenLayerCount, newLayer=True) ## **** ALSO CREATE A NEW NODE ****
            #return the id of the new layer
            return self.hiddenLayerCount
        else:
            self.add_cluster(layer_id, nodeColor)
            return layer_id



    def layersFullyInterconnected(self, layerA_id, layerB_id):
        layers = self.cluster_dict.copy()
        for nodeA_id in layers[layerA_id]["vertices"]:
            for nodeB_id in layers[layerB_id]["vertices"]:
                if nodeB_id not in self.get_vertex(nodeA_id).get_forward_connections():
                    return False
        return True


    def getLayersWithAvailableConnenctions(self):
        ret = []
        layers = self.cluster_dict.copy()
        sortedLayerIDs = sorted(layers.iterkeys())
        for i, layerA_id in enumerate(sortedLayerIDs):
            if i == len(sortedLayerIDs)-1:
                #last iteration (output layer)
                break
            else:
                layerB_id = sortedLayerIDs[i+1]
                #print "Comparing " + str(layerA_id) + " and " + str(layerB_id)
                if not self.layersFullyInterconnected(layerA_id, layerB_id):
                    ret.append((layerA_id, layerB_id))
        return ret




    def add_rand_edge(self):

        availableLayerConnections = self.getLayersWithAvailableConnenctions()
        #print "availableLayerConnections - " + str(availableLayerConnections)

        if len(availableLayerConnections) > 0:
            # select an entry at random
            connectableLayersIndex = random.randint(0,len(availableLayerConnections)-1)
            layer_ids = availableLayerConnections[connectableLayersIndex]
            layerA_id = layer_ids[0]
            layerB_id = layer_ids[1]


            layerA = self.cluster_dict[layerA_id]["vertices"]
            nodeA_id = layerA[random.randint(0,len(layerA)-1)]
            nodeA = self.get_vertex(nodeA_id)


            layerB = self.cluster_dict[layerB_id]["vertices"]
            nodeB_id = layerB[random.randint(0,len(layerB)-1)]

            if nodeB_id not in nodeA.get_forward_connections():
                print "Adding edge (" + nodeA_id + " -> " + nodeB_id + ")"
                self.add_edge(nodeA_id, nodeB_id, random.uniform(0, 1))
                return 1
            else:
                self.add_rand_edge()
        else:
            print "add_rand_edge - Network is fully interconnected, cannot add any more connections"
            return -1



    # CHANGE TO ADD_HIDDEN NODE AND ADD METHODS FOR INPUT AND OUTPUT NODES
    def add_node(self, node_id=None, color=None, layer_id=None, newLayer=None):
        # Returns the id of the created node
        #layer_id is None is handled in clustered_graph
        if node_id is None:
            node_id = self.nodeCount
            ret = self.nodeCount
        else:
            ret = node_id

        newNode = self.add_vertex(str(node_id), layer_id, color)
        if layer_id is not None and layer_id != 0 and layer_id != MAX_INT and newLayer:
            # add an edge either side
            self.add_initial_layer_node_edges(newNode.id, layer_id)
        elif layer_id is not None and layer_id != 0 and layer_id != MAX_INT and not newLayer:
            self.add_initial_node_edges(newNode.id, layer_id)
        self.nodeCount += 1
        return ret




    def add_initial_layer_node_edges(self, node_id, layer_id):
        # Adds random connections to nodes on either side of node_id
        #print self.cluster_dict.keys()
        #print "Index of " + str(layer_id) + ": " + self.cluster_dict.keys().index(layer_id)

        if self.hiddenLayerCount > 1:
            layerA_id = layer_id-1  # previous layer
            node = self.get_vertex(node_id)
            # make all nodes from the previous layer point to this node and copy their connections to node
            for temp_node_id in self.cluster_dict[layerA_id]["vertices"]:
                temp_connections = self.get_vertex(temp_node_id).adjacent
                node.adjacent.update(temp_connections)
                self.get_vertex(temp_node_id).adjacent = {}
                self.add_edge(temp_node_id, node_id)

        else:
            # This is the first hidden layer of the network so we must connect to a random input and output
            # Select a random node from the input layer
            nodeA_id =  self.cluster_dict[0]["vertices"][random.randint(0,len(self.cluster_dict[0]["vertices"])-1   )]
            # Select a random node from the output layer
            nodeB_id =  self.cluster_dict[MAX_INT]["vertices"][random.randint(0,len(self.cluster_dict[MAX_INT]["vertices"])-1   )]
            # connect the nodes
            self.add_edge(nodeA_id, node_id)
            self.add_edge(node_id, nodeB_id)

    def add_initial_node_edges(self, node_id, layer_id):
        # Adds random connections to nodes on either side of node_id
        #print self.cluster_dict.keys()
        #print "Index of " + str(layer_id) + ": " + self.cluster_dict.keys().index(layer_id)
        layerA_id = layer_id-1
        if layer_id == self.cluster_dict.keys()[-2]:
            # layer_id is the second last so layerB is the output
            layerB_id = MAX_INT
        else:
            layerB_id = layer_id+1
        # select a node on each side at random
        nodeA_id = self.cluster_dict[layerA_id]["vertices"][random.randint(0,len(self.cluster_dict[layerA_id]["vertices"])-1)]
        nodeB_id = self.cluster_dict[layerB_id]["vertices"][random.randint(0,len(self.cluster_dict[layerB_id]["vertices"])-1)]
        # make the connection
        self.add_edge(nodeA_id, node_id, random.uniform(0,1))
        self.add_edge(node_id, nodeB_id, random.uniform(0,1))


    def remove_node(self, node_id):
        self.remove_vertex(node_id)



    def propogate_signal(self, dataArr):
        # propagate a signal array forwards through the network

        if len(self.cluster_dict[0]["vertices"]) != len(dataArr):
            print "propogate_signal: dataArr does not match number of input nodes! - Adjusting for this.."

        # give each input the dataArr values
        index = 0
        for in_node_id in self.cluster_dict[0]["vertices"]:
            if index < len(dataArr):
                self.get_vertex.value = dataArr[index]
                index++
            else:
                self.get_vertex.value = 0.0

        for layer_id in range(0, hiddenLayerCount):
            for nodeA_id in self.cluster_dict[layer_id]["vertices"]:
                nodeA = self.get_vertex(nodeA_id)
                for nodeB in nodeA.get_forward_connections():
                    for




    #def mutate(self):
        #newLayerID = self.add_layer()
        #newNodeID = self.add_node(self.nodeId, "pink", "hidden_"+str(newLayerID))
        #print newNodeID
        #self.add_edge(1, newNodeID, 0.223)
        #self.add_edge(newNodeID, 7, 0.3)
        #self.get_vertex("1").remove_neighbour("7")





















if __name__ == "__main__":

    network = Network(4,4)

    for i in range(0,random.randint(1,10)):
        newLayerID = network.add_layer(generate_color())
        for i in range(0, random.randint(0,10)):
            network.add_node(layer_id=newLayerID)

    network.visualise()


    print network
