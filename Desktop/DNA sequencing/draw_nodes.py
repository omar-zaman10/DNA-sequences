from pyvis import network as net
import networkx as nx

def draw_graph(my_graph,label='None',edge_labels=None,name = 'my_net.html',directed =False):
    '''
    Produces a html file with a visualisation of the graph given by the adjacency dictionary
    '''
    if type(my_graph) != dict:
        raise TypeError('Only accepts dict types')

    my_nodes = list(my_graph.keys())

    g = net.Network(directed=directed)

    colors = ['blue']+['red']*(len(my_nodes)-1)
    g.add_nodes(my_nodes,label=label,color=colors) 

    for node in my_nodes:
        neighbours = my_graph[node]
        for i,neighbour in enumerate(neighbours):
            l = edge_labels[i]
            g.add_edge(node,neighbour,label=l,color='grey')
    g.force_atlas_2based()
    #g.barnes_hut()  #this one is good for larger scale
    #g.hrepulsion()
    g.show(name)
    return True


if __name__ == '__main__':
    my_graph = {'A':['B','C','D'],'B':[],'C':[],'D':[]}
    label = [f'( i , j )',f'( i+1 , j )',f'( i+1 , j+1 )',f'( i , j+1 )']
    edge_labels = ['P(deletion)', 'P(transmission)', 'P(insertion)']
    draw_graph(my_graph,label=label,edge_labels=edge_labels,directed=True)