from pyvis import network as net
import networkx as nx

def draw_graph(my_graph,name = 'my_net.html',directed =False):
    '''
    Produces a html file with a visualisation of the graph given by the adjacency dictionary
    '''
    if type(my_graph) != dict:
        raise TypeError('Only accepts dict types')

    my_nodes = list(my_graph.keys())

    g = net.Network(directed=directed)
    g.add_nodes(my_nodes) 
    for node in my_nodes:
        neighbours = my_graph[node]
        for neighbour in neighbours:
            g.add_edge(node,neighbour)
    g.force_atlas_2based()
    #g.barnes_hut()  #this one is good for larger scale
    #g.hrepulsion()
    g.show(name)
    return True


def edges_2_adjacency(edges):
    """Converts edges list [(i,j),(k,l)] etc to adjacency dictionary, assumes undirected graph"""

    adjacency_dict = {}

    for edge in edges:
        [a,b] = edge
        if a not in adjacency_dict.keys():
            adjacency_dict[a] = []
        if b not in adjacency_dict.keys():
            adjacency_dict[b] = []
        adjacency_dict[a].append(b)
        adjacency_dict[b].append(a)

    return adjacency_dict


if __name__ =="__main__":

    my_graph = {'a':['b','c'],'b':['d'],'c': ['e'],'d':['f'],'e': [],'f':[]}
    draw_graph(my_graph,directed=True,name='examplefile.html')

