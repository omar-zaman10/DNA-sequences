import ldpc as ldpc
import numpy as np

c = ldpc.code()
u = np.random.randint(0,2,c.K) #This is the message
x = c.encode(u) #Codeword
#print(np.mod(np.matmul(x,np.transpose(c.pcmat())), 2))
y = 10*(0.5-x) #Input loglikelihoods
print(f'x values {x}')
print(f'y values {y}')
app,it = c.decode(y) #Output loglikelihoods



#print(x)
#print(y)
print(it,app)

print(app == y)