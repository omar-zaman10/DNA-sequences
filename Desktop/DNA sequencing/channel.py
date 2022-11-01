import random

class channel:

    def __init__(self):
        self.input = None
        self.output = None
        self.changes = []
    

    def generate_sequence(self,n=10,bits = False):
        bases = ['A','C','G','T']
        if bits: bases = ['0','1']
        self.input = random.choices(bases,k=n)
        return

    def channel(self,sequence,Pi=0.15,Pd=0.15,Ps=0.15,bits=False):
        Pt = 1-Pi-Pd-Ps
        i,n = 0,len(sequence)
        bases = ['A','C','G','T']
        if bits: bases = ['0','1']
        options = ['transmit','substitute','insert','delete']
        weights = [Pt,Ps,Pi,Pd]
        output =[]
        while i <n:
            choice = random.choices(options,weights=weights)[0]
            #print(i,choice)
            self.changes.append(choice)
            

            if choice == 'transmit':
                output.append(sequence[i])
            elif choice == 'substitute':
                new_choice = bases[:]
                new_choice.remove(sequence[i])
                output.append(random.choice(new_choice))
            elif choice == 'insert':
                output.append(random.choice(bases))
                i-=1
            elif choice == 'delete':
                pass
            i+=1
        self.output = output
        return 

    def generate_input_output(self,n=10,Pi =0,Pd =0,Ps = 0.2,bits=False):
        self.__init__()
        self.generate_sequence(n,bits)
        self.channel(self.input,Pi,Pd,Ps,bits)
        return self.input,self.output


'''Changes needed
1.There could be an infinite number of insertions when reading the sequencer still gives bases even if the end has passed
2. Primer ending codes can be used to check for ending
'''


if __name__ == '__main__':
    c = channel()

    i,o = c.generate_input_output(Pi=0.1,Pd=0.1,n=4,bits = True)

    print(i,o)
    print(c.changes)