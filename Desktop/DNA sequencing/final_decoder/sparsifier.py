import itertools
import numpy as np
class Sparsifier:
    """Sparsifier creates"""

    def __init__(self):
        self.mapping = {} # maps k bit length sequnces to n sparse sequence quaternary vector
        self.binary_sequences = []
        self.reverse_mapping = {} #maps n sparse sequence quaternary vector to k bit length sequnces 
        pass

    def reinitialise(self):
        "Reinitialises the class to sparsify a different mapping"
        self.__init__() 

    def create_mapping(self,k,n):
        """Creates a mapping table between k bits to n sparse quaternary sequence
        in the self.mapping and self.reverse_mapping"""

        #if n < (2**k) / 3: raise ValueError(f'n has to be larger than {(2**k) / 3} for k = {k}')

        def genbin(k, bs=''):
            """Generates all the binary k length sequences"""
            if len(bs) == k:
                self.binary_sequences.append(bs)
            else:
                genbin(k, bs + '0')
                genbin(k, bs + '1')

        genbin(k)

        basis = ('1','2','3')
        index = 0 #Counter for binary numbers

        self.mapping = {bins:None for bins in self.binary_sequences }

        sparse = ['0']*n
        for b in basis:
            for j in range(n):
                
                sparse[j] = b
                self.mapping[self.binary_sequences[index]] = sparse[:]  #''.join(sparse[:])
                sparse[j] = '0'
                index+=1
                if index >= len(self.binary_sequences) : return


        for num in range(2,n):
            new_choices = list(itertools.product(basis,repeat = num))
            points = list(itertools.combinations(range(n),num))

            for new_basis in new_choices:

                for point in points:
                    sparse = ['0']*n

                    for i,choice in zip(point,new_basis):
                        sparse[i] = choice

                    self.mapping[self.binary_sequences[index]] = sparse[:] #''.join(sparse[:])
                    index +=1
                    if index >= len(self.binary_sequences) : return


    def map(self,codeword,k):
        '''Maps codeword to a sparse sequence 
        always choose codeword divisible by k'''
        if len(codeword) % k != 0 : raise ValueError(f'k has to be a divisor the codeword length for sensible mapping')

        sparse_sequence = []
        
        for i in range(0,len(codeword),k):
            bits = codeword[i:i+k]
            sparse_sequence += self.mapping[bits]

        return sparse_sequence

    def sparsify(self,codeword,k,n):
        """Creates the k --> n mapping and maps the codeword onto a sparse sequence"""
        self.create_mapping(k,n)

        return self.map(codeword,k)

    def substitution_distribution(self):
        """Returns the probability distribution for the transmission/substitution 
        at each transmission index -- used to assign the substituion/transmission edge values"""
        pass


if __name__ == '__main__':

    n = 10
    k = 10
    S = Sparsifier()

    S.create_mapping(k,n)
    #print(S.mapping)

    print('-'*162)

    m = np.random.randint(0,2,30) #This is the message
    m = ''.join([str(b) for b in m])
    print(m)

    sparse = S.map(m,k)
    print(len(sparse))


