import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('n=1000_r=25_dna.csv')

errors = df['Average error']
stds = df['SD']
substitions = df['Ps']

#Pi = 0.008
size = len(errors)//3


y1 = errors[0:size]
x1 = substitions[0:size]
y1 = np.array(y1)
sd1 = np.array(stds[0:size])

y2 = errors[size:2*size]
x2 = substitions[size:2*size]
y2 = np.array(y2)
sd2 = np.array(stds[size:2*size])

y3 = errors[2*size:3*size]
x3 = substitions[2*size:3*size]
y3 = np.array(y3)
sd3 = np.array(stds[2*size:3*size])


plt.plot(x1,y1,label = 'Pi = Pd = 0.008',color='b')
plt.fill_between(x1,y1-0.1*sd1,y1+0.1*sd1,color='cornflowerblue')

plt.plot(x2,y2,label = 'Pi = Pd = 0.01',color='y')
plt.fill_between(x1,y2-0.1*sd2,y2+0.1*sd2,color='khaki')

plt.plot(x3,y3,label = 'Pi = Pd = 0.02',color='r')
plt.fill_between(x3,y3-0.1*sd3,y3+0.1*sd3,color='tomato')


plt.xlabel('Probability of substitution')
plt.ylabel('Error percentage %')
plt.title('n = 1000 length sequence')

plt.grid()
plt.legend()
plt.show()
