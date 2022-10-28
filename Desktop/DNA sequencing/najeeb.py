import random
import numpy as np

class photon:
    def __init__(self):
        self.bit = None
        self.base = None
        self.choose_bit_base()

        
    def choose_bit_base(self):
        bits = [1,0]
        bases = ['A','B']
        
        self.bit = random.choices(bits)[0]
        self.base = random.choices(bases)[0]

    


def generate_photon(n=100,cap=101):

    nums = [i for i in range(cap)]

    weights = [np.exp(-1.5*x) for x in range(cap)]
    number_of_photons = random.choices(nums,weights=weights,k=n) #List of pulsees, each entry is number of photons in the pulse


    return number_of_photons


    
'''
for i in range(100):
    a = photon()

    print(a.bit,a.base)
'''