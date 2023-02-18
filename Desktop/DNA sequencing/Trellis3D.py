import random
import matplotlib.pyplot as plt
import numpy as np
import sys
from progress_bar import progress_bar
import time
from channel import channel

transmitted = ['A','C','G','A','C']
recieved = ['A','T','G','C','A']


c = channel()

transmitted,recieved  = c.generate_input_output(Pi=0.1,Pd=0.1,n=4,bits = False)

print(f'transmitted {transmitted} , revceived {recieved}')
print(f'changes {c.changes}')


class Trellis3D:


    def __init__(self,bits=False) :
        self.nodes = [] # List of nodes as their str values, '(i,j,d)'
        self.tuples = {} #Converts from string node to tuple key = string : value = tuple
        self.my_graph = {} # Node and its neighbouring nodes that it leads to  node --> [neighbour]
        self.reverse_graph = {} # Node and its incoming nodes  node <-- [neighbour]
        self.edges = {} # Edge ( str node1, str node2 ) : Gamma value  , gamma is Pi,Pd,Ps


        self.basis = ['A','C','T','G']
        if bits: self.basis = ['1','0']

        self.toor = None
        self.toor_name = None


        self.PI = [0.5,0.1,0.1]  # Distribution Pi, Pd,Ps Pt = 0.3
        self.PD = [0.1,0.5,0.1]
        self.PS = [0.1,0.1,0.1]

        self.alphas = {} #Alphas for each node                 str node : alpha 
        self.betas = {} # Betas for each node                  str node : beta

        self.values = {} # Alpha Gamma Beta for each edge    ( str node1, str node2 ) : value
        self.probabilities = {} # Index of transmitted calculates all the diagonal values to get the P(s) and P(t)
        self.likelihoods = {} #Index of each transmitted with normalised probabilities
        sys.setrecursionlimit(5_000)
        pass


    def forward_backward(self,transmitted,recieved):
        
        depth = [0,-2,2]  # T , I , D  -- Trellis 3rd dimension

        start = time.time()


        #Initialise all the nodes
        for j in range(len(recieved)+1):
            for i in range(len(transmitted)+1):
                for d in depth:
                    if d == -2 and j == 0: continue
                    if d == 2 and i == 0: continue

                    if d == 0 and ((j==0 and i!=0) or (i==0 and j!=0)): continue


                    node = str((i,j,d))
                    self.nodes.append(node)
                    self.tuples[node] = (i,j,d)
                            

        self.toor = (len(transmitted)+2,len(recieved)+2,0)
        self.toor_name = str(self.toor)
        self.nodes.append(self.toor_name)
        self.tuples[self.toor_name] = self.toor

        self.my_graph = {node:[] for node in self.nodes}  # the neighbours directed from the node
        self.reverse_graph = {node:[] for node in self.nodes} #the neighbours directed to the node


        probability_distribution = None

        #Assigning all the neighbours and edges
        for node in self.my_graph:
            i,j,d = self.tuples[node]

            if d == 0: probability_distribution = self.PS
            elif d == -2: probability_distribution = self.PI
            elif d == 2: probability_distribution = self.PD


            Pi,Pd,Ps = probability_distribution

            Pt = round(1 - Pi - Pd - Ps,1)

            #Insertion
            if j+1 <= len(recieved):
                neighbour = str((i,j+1,-2))
                self.my_graph[node].append(neighbour)
                self.edges[(node,neighbour)] = Pi
                self.reverse_graph[neighbour].append(node)

            #Deletion
            if i+1 <= len(transmitted):
                neighbour = str((i+1,j,2))
                self.my_graph[node].append(neighbour)
                self.edges[(node,neighbour)] = Pd
                self.reverse_graph[neighbour].append(node)
            
            #Transmission
            if i+1 <= len(transmitted) and j+1 <= len(recieved):
                neighbour = str((i+1,j+1,0))
                self.my_graph[node].append(neighbour)
                self.reverse_graph[neighbour].append(node)


                if transmitted[i] == recieved[j]:
                    self.edges[(node,neighbour)] = Pt
                else:
                    self.edges[(node,neighbour)] = Ps


        for d in depth:
            node = str((len(transmitted),len(recieved),d))
            self.my_graph[node].append(self.toor_name)
            self.reverse_graph[self.toor_name].append(node)

            self.edges[(node,self.toor_name)] = 1.0

        self.my_graph[self.toor_name] = []        

        print(f'-'*162)

        self.alphas[str((0,0,0))] = 1

        self.counter =0 

        total = len(transmitted)*(len(recieved)+1) + (len(transmitted)+1)*len(recieved) + len(transmitted)*len(recieved) +1

        def forward(node):
            self.counter +=1
            progress_bar(self.counter,total)

            
            if node == str((0,0,0)) : return 1
            if node in self.alphas: 
                return self.alphas[node]

            
            

            neighbours = self.reverse_graph[node]
            output = 0

            for neighbour in neighbours:
                value = self.edges[(neighbour,node)] #neighbour --> node transition
                if neighbour in self.alphas:
                    f = self.alphas[neighbour]
                else:
                    f = forward(neighbour)

                output += f*value
                

            self.alphas[node] = output

            return self.alphas[node]


        print('-'*162)
        self.counter = 0

        forward(self.toor_name)
        print('-'*162)


        self.betas[self.toor_name] = 1.0
        self.counter = 0


        def backward(node):
   

            self.counter +=1
            progress_bar(self.counter,total)

            if node == self.toor_name : return 1.0
            if node in self.betas: 
                return self.betas[node]
            
            

            neighbours = self.my_graph[node]
            output = 0

            for neighbour in neighbours:
                value = self.edges[(node,neighbour)] #neighbour --> node transition
                if neighbour in self.betas: 
                    b = self.betas[neighbour]
                else:
                    b = backward(neighbour)
                output += b*value
                

            self.betas[node] = output

            return self.betas[node]

        starting = str((0,0,0))
    
        backward(starting)
        print('-'*162)

        end = time.time()

        print(f'Time taken for forward backwards algorithm {end-start} seconds with {len(transmitted)} symbols {len(transmitted)**2} squared')

        self.output_likelihoods(transmitted,recieved)

    def output_likelihoods(self,transmitted,recieved):

        self.probabilities = {i:{symbol:0 for symbol in self.basis} for i in range(len(transmitted))}   
        # 0,1,2,3...: {'A': A likelihood, 'C' : C likelihood, ...}

        for edge in self.edges:
            node = edge[0]
            neighbour = edge[1]


            self.values[edge] = self.alphas[node]*self.betas[neighbour]*self.edges[edge]

            node = self.tuples[node] #Converts to tuples
            neighbour = self.tuples[neighbour]

            if node[2] == 0: distribution = self.PS
            elif node[2] == 2: distribution = self.PD
            elif node[2] == -2: distribution = self.PI


            Pi,Pd,Ps = distribution
            Pt = round(1 - Pi - Pd - Ps,1)

            # Havent included deletions horizontal, only does transmissions/substitutions likelihoods
            if node[0]+1 == neighbour[0] and node[1]+1 == neighbour[1]:
                t = transmitted[node[0]]
                r = recieved[node[1]]

                self.probabilities[node[0]][r] += self.values[edge]
        
        for key,symbols_dict in self.probabilities.items():
            s = sum(value for value in symbols_dict.values())

            self.likelihoods[key] = {k:v/s for k,v in symbols_dict.items()}
        
        return self.probabilities
    





    def draw_3D(self,transmitted,recieved):
        #plt.rcParams["figure.figsize"] = [15.0, 15.0]
        plt.rcParams["figure.autolayout"] = True
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        #ax.set_axis_off()


        #Drawing of graph
        colours = True

        for node in self.my_graph:
            i,j,d = self.tuples[node]

            if d ==0: colour = 'red'
            elif d == -2: colour = 'green'
            elif d == 2: colour = 'blue'

            if node == self.toor_name: colour = 'yellow'

            ax.scatter(d, i, j, c=colour,edgecolors='black', s=100)



            alpha = self.alphas[node]
            beta = self.betas[node]

            alpha = round(alpha,4)
            beta = round(beta,4)

            # To draw the alpha values alpha, to replace with coordinates replace alpha with node
            ax.text(d, i, j+0.3,alpha, None)

            neighbours = self.my_graph[node]
            
            for neighbour in neighbours:
                i1,j1,d1 = self.tuples[neighbour]
                x = [i,i1]
                y = [d,d1]
                z = [j,j1]

                colour = 'black'

                if colours:

                    if d ==0: colour = 'red'
                    elif d == -2: colour = 'green'
                    elif d == 2: colour = 'blue'
                    
                ax.plot(y, x, z, c=colour, alpha=0.9)

                prob = self.edges[(node,neighbour)] #Transition probability
                direction = (d1-d,i1-i,j1-j)

                value = self.values[(node,neighbour)]
                value = round(value,4)

                # Labelling the edges with either the transition probabilities or alpha gamma beta 
                #ax.text((3*d+d1)/4.0, (3*i+i1)/4.0, (3*j+j1)/4.0, value, direction)


        for i,symbol in enumerate(transmitted):
            ax.text(0, i+0.5, -0.5,symbol, None,fontweight = 'bold')

        for j,symbol in enumerate(recieved):
            ax.text(0, -0.5, j+0.5,symbol, None,fontweight = 'bold')


        plt.show()
        pass





Trellis = Trellis3D()


Trellis.forward_backward(transmitted,recieved)


print(f'Trellis likelihoods {Trellis.likelihoods}')
Trellis.draw_3D(transmitted,recieved)


'''
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
'''

