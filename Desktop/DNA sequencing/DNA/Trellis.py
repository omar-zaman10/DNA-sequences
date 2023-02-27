from pyvis import network as net
import networkx as nx


class Trellis:

    def __init__(self):

        self.nodes = [] # List of nodes as their str values, '(0,0)'
        self.tuples = {} #Converts from string node to tuple key = string : value = tuple
        self.my_graph = {} # Node and its neighbouring nodes that it leads to  node --> [neighbour]
        self.reverse_graph = {} # Node and its incoming nodes  node <-- [neighbour]
        self.edges = {} # Edge ( str node1, str node2 ) : Gamma value  , gamma is Pi,Pd,Ps
        self.alphas = {} #Alphas for each node                 str node : alpha 
        self.betas = {} # Betas for each node                  str node : beta
        self.values = {} # Alpha Gamma Beta for each edge    ( str node1, str node2 ) : value
        self.probabilities = {} # Index of transmitted calculates all the diagonal values to get the P(s) and P(t)
        self.transitions = {} # Normalises the probabilities  0,1,2,3.. : (p(transmission),p(subsititution)) normalises the probabilities


    def reinitialise(self):
        self.__init__()

    def forward_backward(self,transmitted,recieved,Pi=0.1,Pd=0.1,Ps=0.2):
        self.__init__()

        for j in range(len(recieved)+1):
            for i in range(len(transmitted)+1):
                node = str((i,j))
                self.nodes.append(node)
                self.tuples[node] = (i,j)
                

        self.my_graph = {node:[] for node in self.nodes}  # the neighbours directed from the node
        self.reverse_graph = {node:[] for node in self.nodes} #the neighbours directed to the node
        self.edges = {} #Edge pairs with gammas (probabilities) (node,neighbour) : gamma, nodes are strings



        Pt = round(1 - Pi - Pd - Ps,1)
        for node in self.my_graph:
            i,j = self.tuples[node][0],self.tuples[node][1]

            #Insertion
            if j+1<=len(recieved):
                neighbour = str((i,j+1))
                self.my_graph[node].append(neighbour)
                self.edges[(node,neighbour)] = Pi
                self.reverse_graph[neighbour].append(node)
                

            #Deletion
            if i+1 <=len(transmitted):
                neighbour = str((i+1,j))
                self.my_graph[node].append(neighbour)
                self.edges[(node,neighbour)] = Pd
                self.reverse_graph[neighbour].append(node)

            #Transmission/Substition
            if i+1 <=len(transmitted) and j+1<=len(recieved):
                neighbour = str((i+1,j+1))
                self.my_graph[node].append(neighbour)
                self.reverse_graph[neighbour].append(node)

                if transmitted[i] == recieved[j]:
                    self.edges[(node,neighbour)] = Pt
                else:
                    self.edges[(node,neighbour)] = Ps



        #Dynamic Programming of Forward Backward product sum

        self.alphas = {node:0 for node in self.my_graph}
        self.alphas[self.nodes[0]] = 1


        self.betas = {node:0 for node in self.my_graph}
        self.betas[self.nodes[-1]] = 1

        #Forwards
        for j in range(len(recieved)+1):
            for i in range(len(transmitted)+1):
                node = str((i,j))

                if self.reverse_graph[node]:

                    self.alphas[node] = sum([self.alphas[neighbour]*self.edges[(neighbour,node)] for neighbour in self.reverse_graph[node]])

        #Backwards
        for j in range(len(recieved)+1)[::-1]:
            for i in range(len(transmitted)+1)[::-1]:
                node = str((i,j))

                if self.my_graph[node]:

                    self.betas[node] = sum([self.betas[neighbour]*self.edges[((node,neighbour))] for neighbour in self.my_graph[node]])


        self.values = {} #Edge pairs with alpha gamma beta products 

        self.probabilities = {i:[[],[]] for i in range(len(transmitted))}   # 0,1,2,3...: [[values of transmission],[values of substitions]]



        for edge in self.edges:
            node = edge[0]
            neighbour = edge[1]


            self.values[edge] = self.alphas[node]*self.betas[neighbour]*self.edges[edge]

            node = self.tuples[node] #Converts to tuples
            neighbour = self.tuples[neighbour]

            # Havent included deletions horizontal, only does transmissions/substitutions likelihoods

            if node[0]+1 == neighbour[0] and node[1]+1 == neighbour[1]:
                if self.edges[edge] == Pt:
                    self.probabilities[node[0]][0].append(self.values[edge]) 
                elif self.edges[edge] == Ps:
                    self.probabilities[node[0]][1].append(self.values[edge]) 

            # if -- horizontal deletions


        for key,value in self.probabilities.items():
            t = sum(value[0])
            s = sum(value[1])

            self.transitions[key] = (t/(s+t),s/(s+t))


        return self.transitions

    def draw_trellis(self,transmitted,recieved,name = 'my_net.html',directed =True,Pi=0.1,Pd=0.1,Ps=0.2):
        self.forward_backward(transmitted,recieved,Pi=0.1,Pd=0.1,Ps=0.2)


        '''
        Produces a html file with a visualisation of the graph given by the adjacency dictionary
        '''

        if type(self.my_graph) != dict:
            raise TypeError('Only accepts dict types')

        my_nodes = list(self.my_graph.keys())

        g = net.Network(height = '700px', width = '1400px',directed=directed)
        title = [f'{node} alpha = {self.alphas[node]}  beta = {self.betas[node]}' for node in self.my_graph] 

        g.add_nodes(my_nodes,label=self.nodes,title=title) 

        for node in my_nodes:
            neighbours = self.my_graph[node]
            for neighbour in neighbours:
                n = self.tuples[node]
                d = self.tuples[neighbour]
                weight =10
            
                label = str(self.edges[(node,neighbour)])

                title = f'{self.values[(node,neighbour)]}'


                if n[1] == 0 and d[1] == 0:
                    label = transmitted[n[0]]
                    weight = 12
                    p = self.transitions[n[0]]
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




if __name__ == '__main__':
    
    transmitted = ['A','C','G','A','C']
    recieved = ['A','T','G','C','A']

    T = Trellis()

    print(T.forward_backward(transmitted,recieved))    
    T.draw_trellis(transmitted,recieved,'testing.html')


