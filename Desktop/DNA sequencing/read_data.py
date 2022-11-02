import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('bigger_excel.csv')

errors = df['Average error']
stds = df['SD']
substitions = df['Ps']

#Pi = 0.008
y1 = errors[0:101]
x1 = substitions[0:101]
y1 = np.array(y1)
sd1 = np.array(stds[0:101])

y2 = errors[101:202]
x2 = substitions[101:202]

y3 = errors[202:303]
x3 = substitions[202:303]

plt.plot(x1,y1,label = 'Pi = Pd = 0.008',color='b')
#plt.plot(x1,y1+0.1*sd1,color='b',linestyle='dashed')
#plt.plot(x1,y1-0.1*sd1,color='b',linestyle='dashed')
plt.plot(x2,y2,label = 'Pi = Pd = 0.01',color='y')
plt.plot(x3,y3,label = 'Pi = Pd = 0.02',color='r')

plt.xlabel('Probability of substitution')
plt.ylabel('Error percentage %')


plt.legend()
plt.show()


print(x3)




