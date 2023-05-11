import ldpc as ldpc
import numpy as np
from Trellis3D import Trellis3D
from channel import channel
from sparsifier import Sparsifier
import time
from pprint import pprint



c = ldpc.code(standard='802.16' ,z=15)
m = np.random.randint(0,2,c.K) #This is the message

S = Sparsifier()



x = c.encode(m) #Codeword
codeword = ''.join([str(b) for b in x])


print(codeword)
k,n = 5,5

sparse = S.sparsify(codeword,k,n)

watermark =  np.random.randint(0,4,len(sparse))


transmitted = (sparse + watermark) % 4



bases_mapping = {0:'A', 1:'C', 2:'G', 3:'T'}
transmitted = [bases_mapping[q] for q  in transmitted]


C = channel()


PI = [0.5,0,0.2]
PD = [0.0,0.5,0.02]
PS = [0.02,0.02,0.2]

r = C.bigram_channel(transmitted,PI=PI,PD=PD,PS=PS)

pprint(sparse)


sparse_distribution = S.substitution_distribution(k,n)
print(sparse_distribution)

"""


#transmitted,recieved  = c.generate_bigram_input_output(n=500,bits = False,PI=PI,PD=PD,PS=PS)


#print(np.mod(np.matmul(x,np.transpose(c.pcmat())), 2))
#y = 10*(0.5-x) #Input loglikelihoods
#print(len(x))
#print(f'x values {x}')
#print(f'y values {y}')
#app,it = c.decode(y) #Output loglikelihoods

"""


'''

transmitted = ['A','C','G','A','C']
recieved = ['A','T','G','C','A']


c = channel()
start = time.time()

PI = [0.5,0.02,0.2]
PD = [0.02,0.5,0.02]
PS = [0.02,0.02,0.2]

#transmitted,recieved  = c.generate_bigram_input_output(n=500,bits = False,PI=PI,PD=PD,PS=PS)

#print(f'transmitted {transmitted} , revceived {recieved}')
#print(f'changes {c.changes}')



Trellis3d = Trellis3D()


#Trellis3d.forward_backward(transmitted,recieved,PI=PI,PD=PD,PS=PS)
#Trellis3d.draw_3D(transmitted,recieved)






#print(x)
#print(y)
print(it,app)

print(app == y)
'''