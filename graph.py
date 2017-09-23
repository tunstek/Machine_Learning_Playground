
import graphviz as gv


from functions import *




class Vertex(object):
    def __init__(self, node, color=None, clusterID=None):
        if clusterID is None:
            clusterID = ""

        self.id = node
        self.adjacent = {} # Dict of neighbouring node edge weights keyed by the neighbour node id
        self.clusterID = clusterID
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
        self.num_vertices = 0


    def __iter__(self):
        return iter(self.vert_dict.values())


    def __str__(self):
        # Returns a str representation of the graph
        ret = ""
        for vid, v in self.vert_dict.iteritems():
            for w in v.get_connections():
                w_node = self.vert_dict[w]
                wid = w_node.get_id()
                ret = ret + '( %s , %s, %f)'  % ( vid, wid, v.get_weight(w)) + "\n"

        for v in self:
            ret = ret + '%s' %(self.vert_dict[v.get_id()]) + "\n"
        return ret


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


        #vis.attr('edge', constraint="false")


        visited = []
        # sort vertices into clusters
        clusters = {}
        for v_id in self.vert_dict.keys():
            v = self.vert_dict[v_id]
            try:
                clusters[v.clusterID].append(v_id)
            except KeyError:
                clusters[v.clusterID] = []
                clusters[v.clusterID].append(v_id)

        for key in clusters:
            for node_id in clusters[key]:
                temp = gv.Digraph(name='cluster_'+str(key))
                node = self.vert_dict[node_id]
                temp.node(str(node_id), color=node.color)

                temp.graph_attr.update(rankdir='LR')

                if key == "Inputs":
                    temp.graph_attr.update(rank='min')
                    temp.graph_attr.update(label='Inputs')
                elif key == "Outputs":
                    temp.graph_attr.update(label='Outputs')
                    temp.graph_attr.update(rank='max')
                else:
                    temp.graph_attr.update(label='cluster_'+str(key))
                    temp.graph_attr.update(rank=str(key))
                vis.subgraph(temp)

        # make all the connections
        for key in clusters:
            for nodeA_id in clusters[key]:
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



    def add_vertex(self, node_id, color=None, clusterID=None):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node_id, color, clusterID)
        self.vert_dict[node_id] = new_vertex
        return new_vertex

    def remove_vertex(self, node_id):
        self.num_vertices = self.num_vertices - 1
        self.vert_dict.pop(node_id)

    def get_vertex(self, n_id):
        if n_id in self.vert_dict:
            return self.vert_dict[n_id]
        else:
            return None


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
            print "ERR: add_edge - vertex " + frm + " doesn't exist!\nCreating node.."
            self.add_vertex(frm)
        if to not in self.vert_dict:
            print "ERR: add_edge - vertex " + to + " doesn't exist!\nCreating node.."
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbour(to, cost)
        #self.vert_dict[to].add_neighbour(frm, cost)


    def get_vertices(self):
        return self.vert_dict.keys()




if __name__ == '__main__':

    import random


    g = Graph()

    g.add_vertex('a', "blue", "Inputs")
    g.add_vertex('b', "blue", "Inputs")
    g.add_vertex('c', "blue", "Inputs")
    g.add_vertex('d', "red", "Outputs")
    g.add_vertex('e', "red", "Outputs")
    g.add_vertex('f', "red", "Outputs")

    g.add_vertex('g', "purple", 0) # Use numbers to define hidden clusters
    g.add_vertex('h', "purple", 0) # Use numbers to define hidden clusters

    g.add_vertex('i', "pink", 1) # Use numbers to define hidden clusters


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

    #print g.get_vertex("c")
    g.get_vertex("c").remove_neighbour("d")
    g.add_edge("c","g",0.234)

    g.add_edge("g","i", 0.243)

    g.add_edge("i","d",0.234)





    print g

    g.visualise()
