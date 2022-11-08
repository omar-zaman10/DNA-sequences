from pyvis import network as net
import networkx as nx

def draw_trellis(my_graph,tuples,recieved,transmitted,edges,alphas,betas,values,transitions,name = 'my_net.html',directed =True):
    '''
    Produces a html file with a visualisation of the graph given by the adjacency dictionary
    '''
    if type(my_graph) != dict:
        raise TypeError('Only accepts dict types')

    my_nodes = list(my_graph.keys())

    g = net.Network(height = '700px', width = '1400px',directed=directed)
    title = [f'{node} alpha = {alphas[node]}  beta = {betas[node]}' for node in my_graph] 

    g.add_nodes(my_nodes,label=nodes,title=title) 

    for node in my_nodes:
        neighbours = my_graph[node]
        for neighbour in neighbours:
            n = tuples[node]
            d = tuples[neighbour]
            weight =10
        
            label = str(edges[(node,neighbour)])

            title = f'{values[(node,neighbour)]}'


            if n[1] == 0 and d[1] == 0:
                label = transmitted[n[0]]
                weight = 12
                p = transitions[n[0]]
                title = title + f' transmission = {p[0]}, substitution = {p[1]}'

            elif n[0] == 0 and d[0] == 0:
                label =recieved[n[1]]
                weight = 11
                        

            

            g.add_edge(node,neighbour,label=label,value=weight,title=title)
    g.force_atlas_2based()
    #g.barnes_hut()  #this one is good for larger scale
    #g.hrepulsion()
    g.show(name)
    return True


transmitted = ['A','C','G','A']
recieved = ['A','T','G','C','A']

nodes = []
tuples = {}  #Converts between tuple node and string node with key being str


for j in range(len(recieved)+1):
    for i in range(len(transmitted)+1):
        node = str((i,j))
        nodes.append(node)
        tuples[node] = (i,j)
        


my_graph = {node:[] for node in nodes}  # the neighbours directed from the node
reverse_graph = {node:[] for node in nodes} #the neighbours directed to the node
edges = {} #Edge pairs with gammas (probabilities) (node,neighbour) : gamma, nodes are strings


'''Viterbi edges'''

Pi = 0.1
Pd = 0.1
Ps = 0.2
Pt = round(1 - Pi - Pd - Ps,1)

for node in my_graph:
    i,j = tuples[node][0],tuples[node][1]

    #Insertion
    if j+1<=len(recieved):
        neighbour = str((i,j+1))
        my_graph[node].append(neighbour)
        edges[(node,neighbour)] = Pi
        reverse_graph[neighbour].append(node)
        

    #Deletion
    if i+1 <=len(transmitted):
        neighbour = str((i+1,j))
        my_graph[node].append(neighbour)
        edges[(node,neighbour)] = Pd
        reverse_graph[neighbour].append(node)

    #Transmission/Substition
    if i+1 <=len(transmitted) and j+1<=len(recieved):
        neighbour = str((i+1,j+1))
        my_graph[node].append(neighbour)
        reverse_graph[neighbour].append(node)

        if transmitted[i] == recieved[j]:
            edges[(node,neighbour)] = Pt
        else:
            edges[(node,neighbour)] = Ps



#Dynamic Programming of Viterbi product max

alphas = {node:0 for node in my_graph}
alphas[nodes[0]] = 1


betas = {node:0 for node in my_graph}
betas[nodes[-1]] = 1


for j in range(len(recieved)+1):
    for i in range(len(transmitted)+1):
        node = str((i,j))

        if reverse_graph[node]:

            alphas[node] = max([alphas[neighbour]*edges[(neighbour,node)] for neighbour in reverse_graph[node]])


for j in range(len(recieved)+1)[::-1]:
    for i in range(len(transmitted)+1)[::-1]:
        node = str((i,j))

        if my_graph[node]:

            betas[node] = max([betas[neighbour]*edges[((node,neighbour))] for neighbour in my_graph[node]])


values = {} #Edge pairs with alpha gamma beta products 

probabilities = {i:[[],[]] for i in range(len(transmitted))}   # 0,1,2,3...: [[values of transmission],[values of substitions]]

transitions = {} # 0,1,2,3.. : (p(transmission),p(subsititution)) normalises the probabilities


for edge in edges:
    node = edge[0]
    neighbour = edge[1]


    values[edge] = alphas[node]*betas[neighbour]*edges[edge]

    node = tuples[node] #Converts to tuples
    neighbour = tuples[neighbour]



    if node[0]+1 == neighbour[0] and node[1]+1 == neighbour[1]:
        if edges[edge] == Pt:
            probabilities[node[0]][0].append(values[edge]) 
        elif edges[edge] == Ps:
            probabilities[node[0]][1].append(values[edge]) 


for key,value in probabilities.items():
    t = sum(value[0])
    s = sum(value[1])

    transitions[key] = (t/(s+t),s/(s+t))

print(transitions)




if __name__ == '__main__':

    draw_trellis(my_graph,tuples,recieved,transmitted,edges,alphas,betas,values,transitions,name='viterbi_max_with_gamma_transitions.html',directed=True)
