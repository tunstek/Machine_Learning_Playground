
import graphviz as gv
import sys

from functions import *

MAX_INT = sys.maxint

# input layer is always 0
# output layer is always MAX_INT


class Vertex(object):
    def __init__(self, node, color=None, clusterID=None):
        if clusterID is None:
            clusterID = ""
        if color is None:
            color = "black"
        self.id = node
        self.cluster_id = clusterID
        self.adjacent = {} # Dict of neighbouring node edge weights keyed by the neighbour node id
        self.color = color


    def __str__(self):
        #return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])
        return str(self.id) + ' adjacent: ' + str(self.adjacent.keys())


    def add_neighbour(self, neighbour_id, weight=0.0):
        self.adjacent[neighbour_id] = float(weight)

    def remove_neighbour(self, neighbour_id):
        self.adjacent.pop(neighbour_id)

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor_id):
        return self.adjacent[neighbor_id]

    def change_weight(self, neighbor_id, weight):
        self.adjacent[neighbor_id] = float(weight)



class Graph(object):
    def __init__(self):
        self.vert_dict = {} # A dict of vertices contained in the graph keyed by their ids
        self.cluster_dict = {} # A dict of cluster attributes and assigned vertices keyed by cluster ids
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def __str__(self):
        # Returns a str representation of the graph
        ret = "\nWeights:\n\n"
        for vid, v in self.vert_dict.iteritems():
            for w in v.get_connections():
                w_node = self.vert_dict[w]
                wid = w_node.get_id()
                ret = ret + '( %s , %s, %f)'  % ( vid, wid, v.get_weight(w)) + "\n"
        ret = ret + "\nAdjecent Vertices:\n\n"
        for v in self:
            ret = ret + '%s' %(self.vert_dict[v.get_id()]) + "\n"
        ret = ret + "\nClusters:\n\n"
        for key in self.cluster_dict:
            if key == 0:
                str_key = "inputs"
            elif key == MAX_INT:
                str_key = "outputs"
            else:
                str_key = "layer_"+str(key)
            ret = ret + str_key + ":\n{"
            for vertex_id in self.cluster_dict[key]["vertices"]:
                ret = ret + " " + vertex_id + " "
            ret = ret + "}\n"
            #ret = ret + "color - " + self.cluster_dict[key]["color"] + "\n"
        return ret

    def get_cluster(self, c_id):
        if c_id in self.cluster_dict:
            return self.cluster_dict[c_id]
        else:
            return None

    def get_vertices(self):
        return self.vert_dict.keys()
    def get_vertex(self, n_id):
        if n_id in self.vert_dict:
            return self.vert_dict[n_id]
        else:
            return None


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


        for key in self.cluster_dict:
            for node_id in self.cluster_dict[key]["vertices"]:
                temp = gv.Digraph(name='cluster_'+str(key))
                node = self.vert_dict[node_id]

                # CLUSTER COLOR TRUMPS NODE COLOR
                if node.color != "black":
                    temp.node(str(node_id), color=node.color)
                if self.cluster_dict[key]["color"] != "black":
                    temp.node(str(node_id), color=self.cluster_dict[key]["color"])


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
                vis.subgraph(temp)

        # make all the connections
        for key in self.cluster_dict:
            for nodeA_id in self.cluster_dict[key]["vertices"]:
                nodeA = self.vert_dict[nodeA_id]
                for nodeB_id in nodeA.get_connections():
                    nodeB = self.vert_dict[nodeB_id]
                    weight = nodeA.get_weight(nodeB_id)
                    vis.edge(nodeA.id, nodeB.id)
                    #if type(weight) == float:
                        # TRUNCATE WEIGHT FOR READABILITY
                        #vis.edge(nodeA.id, nodeB.id, label=str('%.3f'%(weight)))
                        #vis.edge(nodeA.id, nodeB.id)
                    #else:
                        #vis.edge(nodeA.id, nodeB.id, label=str(weight))

        vis.render('img/g1.gv', view=True)


    def add_cluster(self, cluster_id, color=None):
        self.cluster_dict[cluster_id] = {}
        self.cluster_dict[cluster_id]["vertices"] = []
        if color is None:
            color = "black"
        self.cluster_dict[cluster_id]["color"] = color

    def add_vertex_to_cluster(self, vertex_id, cluster_id):
        # presuming the cluster already exists
        try:
            self.cluster_dict[cluster_id]["vertices"].append(vertex_id)
        except KeyError:
            print str(cluster_id) + " cluster doesn't exist, creating new cluster.."
            self.add_cluster(cluster_id)
            self.cluster_dict[cluster_id]["vertices"].append(vertex_id)


    def add_vertex(self, vertex_id, clusterID=None, color=None, ):
        # RETURNS (Vertex, clusterID)
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(vertex_id, color)
        self.vert_dict[vertex_id] = new_vertex
        if clusterID is not None:
            self.add_vertex_to_cluster(vertex_id, clusterID)
        return new_vertex

    def remove_vertex(self, node_id):
        self.num_vertices = self.num_vertices - 1
        self.vert_dict.pop(node_id)
        # remove vertex from all clusters
        for key in self.cluster_dict:
            self.cluster_dict[key]["vertices"].pop(node_id)




    def remove_edge(self, frm_id, to_id):
        if frm_id in self.vert_dict: #and to_id in self.vert_dict:
            self.vert_dict[frm_id].remove_neighbour(self.vert_dict[to_id])
            #self.vert_dict[to_id].remove_neighbour(self.vert_dict[frm_id])
            return 1
        else:
            return -1


    def add_edge(self, frm_id, to_id, cost=0):
        frm = str(frm_id)
        to = str(to_id)
        if frm not in self.vert_dict:
            print "ERR: add_edge - vertex " + frm + " doesn't exist!"
            exit()
            #self.add_vertex(frm)
        if to not in self.vert_dict:
            print "ERR: add_edge - vertex " + to + " doesn't exist!"
            exit()
            #self.add_vertex(to)

        self.vert_dict[frm].add_neighbour(to, cost)
        #self.vert_dict[to].add_neighbour(frm, cost)







if __name__ == '__main__':

    import random


    g = Graph()

    g.add_vertex('a', 0)
    g.add_vertex('b', 0)
    g.add_vertex('c', 0)
    g.add_vertex('d', MAX_INT)
    g.add_vertex('e', MAX_INT)
    g.add_vertex('f', MAX_INT)

    g.add_vertex('g', 1)
    g.add_vertex('h', 1)

    g.add_vertex('i', 2)

    #g.add_vertex('g', "purple", 0) # Use numbers to define hidden clusters
    #g.add_vertex('h', "purple", 0) # Use numbers to define hidden clusters

    #g.add_vertex('i', "pink", 1) # Use numbers to define hidden clusters


    #pdb.set_trace()

    g.add_edge('a', 'd', random.uniform(0,1))
    g.add_edge('a', 'e', random.uniform(0,1))
    g.add_edge('a', 'f', random.uniform(0,1))
    g.add_edge('b', 'd', random.uniform(0,1))
    g.add_edge('b', 'e', random.uniform(0,1))
    g.add_edge('b', 'f', random.uniform(0,1))
    g.add_edge('c', 'd', random.uniform(0,1))
    g.add_edge('c', 'e', random.uniform(0,1))
    g.add_edge('c', 'f', random.uniform(0,1))

    print g.get_vertex("c")
    g.get_vertex("c").remove_neighbour("d")
    g.add_edge("c","g",0.234)

    g.add_edge("g","i", 0.243)

    g.add_edge("i","d",0.234)





    print g

    g.visualise()
