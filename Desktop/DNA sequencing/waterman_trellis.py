from pyvis import network as net
import networkx as nx

def draw_trellis(my_graph,tuples,recieved,transmitted,edges,alphas,name = 'my_net.html',directed =True):
    '''
    Produces a html file with a visualisation of the graph given by the adjacency dictionary
    '''
    if type(my_graph) != dict:
        raise TypeError('Only accepts dict types')

    my_nodes = list(my_graph.keys())

    g = net.Network(directed=directed)
    title = [f'{node}  {alphas[node]}' for node in my_graph] 
    print(title)

    g.add_nodes(my_nodes,label=title,title=title) 

    for node in my_nodes:
        neighbours = my_graph[node]
        for neighbour in neighbours:
            n = tuples[node]
            d = tuples[neighbour]
            weight =10
            #Overrides label as waterman schmidt edit distance
            label = str(edges[(node,neighbour)])
            if n[1] == 0 and d[1] == 0:
                label = transmitted[n[0]]
                weight = 12

            elif n[0] == 0 and d[0] == 0:
                label =recieved[n[1]]
                weight = 11
                
        

            

            g.add_edge(node,neighbour,label=label,value=weight)
    g.force_atlas_2based()
    #g.barnes_hut()  #this one is good for larger scale
    #g.hrepulsion()
    g.show(name)
    return True


transmitted = ['A','C','G']
recieved = ['A','T','C','G']

nodes = []
tuples = {}


for j in range(len(recieved)+1):
    for i in range(len(transmitted)+1):
        node = str((i,j))
        nodes.append(node)
        tuples[node] = (i,j)
        


my_graph = {node:[] for node in nodes}  # the neighbours directed from the node
reverse_graph = {node:[] for node in nodes} #the neighbours directed to the node
edges = {}

'''Waterman Schmidt edges'''

for node in my_graph:
    i,j = tuples[node][0],tuples[node][1]

    #Insertion
    if j+1<=len(recieved):
        neighbour = str((i,j+1))
        my_graph[node].append(neighbour)
        edges[(node,neighbour)] = 1
        reverse_graph[neighbour].append(node)
        

    #Deletion
    if i+1 <=len(transmitted):
        neighbour = str((i+1,j))
        my_graph[node].append(neighbour)
        edges[(node,neighbour)] = 1
        reverse_graph[neighbour].append(node)

    #Transmission/Substition
    if i+1 <=len(transmitted) and j+1<=len(recieved):
        neighbour = str((i+1,j+1))
        my_graph[node].append(neighbour)
        reverse_graph[neighbour].append(node)

        if transmitted[i] == recieved[j]:
            edges[(node,neighbour)] = 0
        else:
            edges[(node,neighbour)] = 1



#Dynamic Programming

alphas = {node:0 for node in my_graph}

for j in range(len(recieved)+1):
    for i in range(len(transmitted)+1):
        node = str((i,j))

        if reverse_graph[node]:

            alphas[node] = min([alphas[neighbour]+edges[(neighbour,node)] for neighbour in reverse_graph[node]])

     

if __name__ == '__main__':

    draw_trellis(my_graph,tuples,recieved,transmitted,edges,alphas,name='new_file.html',directed=True)