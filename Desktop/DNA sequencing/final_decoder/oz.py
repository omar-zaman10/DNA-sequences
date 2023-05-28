import ldpc as ldpc
import numpy as np
from Trellis3D import Trellis3D
from channel import channel
from sparsifier import Sparsifier
import time
from pprint import pprint



c = ldpc.code(standard='802.16' ,z=10,rate = '1/2')
m = np.random.randint(0,2,c.K) #This is the message

print(m, len(m))
S = Sparsifier()


x = c.encode(m) #Codeword
codeword = ''.join([str(b) for b in x])

print(f'Length of codeword {len(codeword)}')


k,n = 4,4

#pprint(codeword)

sparse = S.sparsify(codeword,k,n)

print(sparse)

watermark =  np.random.randint(0,4,len(sparse))

transmitted = (sparse + watermark) % 4


bases_mapping = {0:'A', 1:'C', 2:'G', 3:'T'}
transmitted = [bases_mapping[q] for q  in transmitted]

print(f'Length of transmitted {len(transmitted)}')


C = channel()


ps = 0.00
pti = 0.02
ptd = 0.02

PI = [0.5,0.0,ps]
PD = [0.0,0.5,ps]
PS = [pti,ptd,ps]

recieved = C.bigram_channel(transmitted,PI=PI,PD=PD,PS=PS)


#print(recieved)
print(f'Length of received {len(recieved)}')


sparse_distribution = S.substitution_distribution(k,n)

#print('sparse distribution',sparse_distribution)


watermark = [bases_mapping[q] for q  in watermark]
#print('watermark',watermark)

Trellis3d = Trellis3D(sparse_distribution)


transmitted_likelihoods = Trellis3d.forward_backward(watermark,recieved,PI=PI,PD=PD,PS=PS)
#print(f'Trellis likelihoods {transmitted_likelihoods}')


codeword_likelihoods = S.decoder(transmitted_likelihoods,watermark,k,n)


app,it = c.decode(codeword_likelihoods) #Output loglikelihoods




#pprint(app)

codeword_estimate = ['0' if a>0 else '1' for a in app  ]
codeword_estimate = ''.join(codeword_estimate)

#print(codeword_estimate)

print(codeword == codeword_estimate)


o = [a[0] == a[1] for a in zip(codeword,codeword_estimate)]

print(o.count(True) *100.0/ len(o))

print(list(codeword_estimate[:len(m)])) # m estimate