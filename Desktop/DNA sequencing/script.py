import numpy as np
import random
import matplotlib

f= open("mytext.txt","w+")

for i in range(10):
    j = random.randint(100*i,100*(i+1))

    f.write(f'Hello World {j}\n')

f.close()
