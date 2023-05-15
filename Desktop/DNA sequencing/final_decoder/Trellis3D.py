import random
import matplotlib.pyplot as plt
import numpy as np
import sys
from progress_bar import progress_bar
import time
from channel import channel
from sparsifier import Sparsifier


class Trellis3D:


    def __init__(self,sparse_distribution,bits=False) :
        self.nodes = [] # List of nodes as their str values, '(i,j,d)'
        self.tuples = {} #Converts from string node to tuple key = string : value = tuple
        self.my_graph = {} # Node and its neighbouring nodes that it leads to  node --> [neighbour]
        self.reverse_graph = {} # Node and its incoming nodes  node <-- [neighbour]
        self.edges = {} # Edge ( str node1, str node2 ) : Gamma value  , gamma is Pi,Pd,Ps


        self.basis = ['A','C','T','G']
        if bits: self.basis = ['1','0']

        self.toor = None
        self.toor_name = None


        self.PI = None #[0.5,0.02,0.2]  # Distribution Pi, Pd,Ps Pt = 0.3
        self.PD = None #[0.02,0.5,0.02]
        self.PS = None #[0.02,0.02,0.2]

        self.alphas = {} #Alphas for each node                 str node : alpha 
        self.betas = {} # Betas for each node                  str node : beta

        self.values = {} # Alpha * Gamma * Beta for each edge    ( str node1, str node2 ) : value
        self.probabilities = {} # Unnormalised probabilities for each transmitted index {0: {A:pA ... T:pT }, 1 :{} , .... }
        self.likelihoods = {} #Index of each transmitted with normalised probabilities
        #sys.setrecursionlimit(5_000)

        self.q_mapping  = {0:'A', 1:'C', 2:'G', 3:'T'}
        self.base_mapping = {'A':0, 'C':1, 'G':2, 'T':3}
        self.sparse_distribution = sparse_distribution
        


    def forward_backward(self,watermark,recieved,PI,PD,PS):

        startup = time.time()
        
        #Initialise probability distributions
        self.PI = PI
        self.PD = PD
        self.PS = PS
        
        depth = [0,-2,2]  # T , I , D  -- Trellis 3rd dimension

        start = time.time()


        #Initialise all the nodes
        for j in range(len(recieved)+1):
            for i in range(len(watermark)+1):
                for d in depth:
                    if d == -2 and j == 0: continue
                    if d == 2 and i == 0: continue

                    if d == 0 and ((j==0 and i!=0) or (i==0 and j!=0)): continue


                    node = str((i,j,d))
                    self.nodes.append(node)
                    self.tuples[node] = (i,j,d)
            

        self.toor = (len(watermark)+2,len(recieved)+2,0)
        self.toor_name = str(self.toor)
        self.nodes.append(self.toor_name)
        self.tuples[self.toor_name] = self.toor

        self.my_graph = {node:[] for node in self.nodes}  # the neighbours directed from the node
        self.reverse_graph = {node:[] for node in self.nodes} #the neighbours directed to the node


        probability_distribution = None
        n = len(self.sparse_distribution)

        #print(f'Time taken for initialising the nodes {time.time() - startup}s')
        start = time.time()


        #Assigning all the neighbours and edges
        for node in self.my_graph:
            i,j,d = self.tuples[node]

            if d == 0: probability_distribution = self.PS
            elif d == -2: probability_distribution = self.PI
            elif d == 2: probability_distribution = self.PD

            Pi,Pd,Ps = probability_distribution
            #Ps is now affected by the sparse distrubution and similarly for Pt


            normalisation = 1-Pi-Pd # Probability for transmission/substitution

            #Insertion
            if j+1 <= len(recieved):
                neighbour = str((i,j+1,-2))
                self.my_graph[node].append(neighbour)
                self.edges[(node,neighbour)] = Pi
                self.reverse_graph[neighbour].append(node)

            #Deletion
            if i+1 <= len(watermark):
                neighbour = str((i+1,j,2))
                self.my_graph[node].append(neighbour)
                self.edges[(node,neighbour)] = Pd
                self.reverse_graph[neighbour].append(node)
            
            #Transmission
            if i+1 <= len(watermark) and j+1 <= len(recieved):
                neighbour = str((i+1,j+1,0))
                self.my_graph[node].append(neighbour)
                self.reverse_graph[neighbour].append(node)

                ti = self.base_mapping[watermark[i]] 
                ri = self.base_mapping[recieved[j]]
                di = str((ri-ti)%4)

                #Normalise these in accordance to transmissions
                #Is normalisation necessary?

                self.edges[(node,neighbour)] =  normalisation*self.sparse_distribution[i%n][di]


        for d in depth:
            node = str((len(watermark),len(recieved),d))
            self.my_graph[node].append(self.toor_name)
            self.reverse_graph[self.toor_name].append(node)

            self.edges[(node,self.toor_name)] = 1.0

        self.my_graph[self.toor_name] = []        


        self.alphas[str((0,0,0))] = 1

        self.counter =0 

        total = len(watermark)*(len(recieved)+1) + (len(watermark)+1)*len(recieved) + len(watermark)*len(recieved) +1

        #print(f'Time taken for initialising the edges {time.time() - start}s')
        
        


        def forward(node):
            '''Forward algorithm using recursion'''
            self.counter +=1
            #progress_bar(self.counter,total)

            
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


        def forward_stack():
            '''Forward algorithm using a stack instead of recursive stack'''
            stack = [self.toor_name]
            order = [str((0,0,0))]

            while stack:
                node = stack[-1]
                neighbours = self.reverse_graph[node]

                mylist = [neighbour in self.alphas for neighbour in neighbours]
                if all(mylist):
                    f = 0
                    for neighbour in neighbours:
                        value = self.edges[(neighbour,node)] # neighbour --> node
                        f += value*self.alphas[neighbour]
                    self.alphas[node] = f
                    stack.pop(-1)
                    order.append(node)
                
                else:
                    for neighbour in neighbours:
                        if neighbour not in self.alphas: stack.append(neighbour)

            return order

        #start1 = time.time()
        #forward(self.toor_name)
        #print(f'Time taken for recursion {time.time() - start1}s')


        start2 = time.time()
        order = forward_stack()
        #print(f'Time taken for forward stack {time.time() - start2}s')

     

        self.betas[self.toor_name] = 1.0
        self.counter = 0
        
        

        def backward(node):

            self.counter +=1
            #progress_bar(self.counter,total)

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



        def backward_stack():
            '''Forward algorithm using a stack instead of recursive stack'''
            stack = [str((0,0,0))] 
            reverse_order = [self.toor_name]

            while stack:
                node = stack[-1]
                neighbours = self.my_graph[node]

                mylist = [neighbour in self.betas for neighbour in neighbours]
                if all(mylist):
                    b = 0
                    for neighbour in neighbours:
                        value = self.edges[(node,neighbour)] # node --> neighbour
                        b += value*self.betas[neighbour]
                    self.betas[node] = b
                    stack.pop(-1)
                    reverse_order.append(node)
                
                else:
                    for neighbour in neighbours:
                        if neighbour not in self.betas: stack.append(neighbour)

            return reverse_order


        #starting = str((0,0,0))
        #backward(starting)

        start3 = time.time()
        reverse_order = backward_stack()
        #print(f'Time taken for backwards stack {time.time() - start3}s')


        start4 = time.time()
        #print(f'Time taken for forward backwards algorithm {end-start} seconds with {len(watermark)} symbols {len(watermark)**2} squared')
        self.output_likelihoods(watermark,recieved)

        #print(f'time taken for likelihoods calculations {time.time() - start4}s with {len(self.edges)} number of edges and nodes {total}')
        return self.likelihoods

    def output_likelihoods(self,watermark,recieved):

        self.probabilities = {i:{symbol:0 for symbol in self.basis} for i in range(len(watermark))}   
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
                r = recieved[node[1]]
                self.probabilities[node[0]][r] += self.values[edge]

            # Deletions horizontal transitions

            if node[0]+1 == neighbour[0] and node[1] == neighbour[1]:
                w = watermark[node[0]]

                for q in self.sparse_distribution[node[0]%len(self.sparse_distribution)]:
                    p = self.values[edge]*self.sparse_distribution[node[0]%len(self.sparse_distribution)][q]


                    t = (self.base_mapping[w] +int(q)) % 4

                    self.probabilities[node[0]][self.q_mapping[t]] += p


        
        for key,symbols_dict in self.probabilities.items():
            s = sum(value for value in symbols_dict.values())

            self.likelihoods[key] = {k:v/s for k,v in symbols_dict.items()}

        
    def draw_3D(self,watermark,recieved):
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
            #ax.text(d, i, j+0.3,alpha, None)

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
                if i1 == i+1 and j1 == j+1:
                    ax.text((3*d+d1)/4.0, (3*i+i1)/4.0, (3*j+j1)/4.0, round(prob,4), direction)


        for i,symbol in enumerate(watermark):
            ax.text(0, i+0.5, -0.5,symbol, None,fontweight = 'bold')

        for j,symbol in enumerate(recieved):
            ax.text(0, -0.5, j+0.5,symbol, None,fontweight = 'bold')


        plt.show()




if __name__ == '__main__':

    codeword = np.random.randint(0,2,5)
    codeword = ''.join([str(b) for b in codeword])


    S = Sparsifier()
    k,n = 5,10

    sparse = S.sparsify(codeword,k,n)
    sparse_distribution = S.substitution_distribution(k,n)
    print(sparse_distribution)

    watermark =  np.random.randint(0,4,len(sparse))


    transmitted = (sparse + watermark) % 4
    
    print(sparse)

    #print(sparse_distribution)

    #transmitted = ['A','C','G','A','C']
    #recieved = ['A','T','G','C','A']

    bases_mapping = {0:'A', 1:'C', 2:'G', 3:'T'}
    transmitted = [bases_mapping[q] for q  in transmitted]
    watermark = [bases_mapping[q] for q  in watermark]
    print(watermark)
    print(transmitted)


    c = channel()
    start = time.time()

    PI = [0.5,0.0,0.02] # No probability of deletion
    PD = [0.0,0.5,0.02] # No probability of insertion
    PS = [0.1,0.1,0.02]

    #transmitted,recieved  = c.generate_bigram_input_output(n=5,bits = False,PI=PI,PD=PD,PS=PS)

    #print(f'transmitted {transmitted} , revceived {recieved}')
    #print(f'changes {c.changes}')

    recieved = c.bigram_channel(transmitted,PI=PI,PD=PD,PS=PS)

    print(recieved)


    Trellis3d = Trellis3D(sparse_distribution)


    Trellis3d.forward_backward(watermark,recieved,PI=PI,PD=PD,PS=PS)
    print(f'Time taken {time.time()-start}s')
    print(f'Trellis likelihoods {Trellis3d.likelihoods}')

    #Trellis3d.draw_3D(watermark,recieved)

    


    
    
