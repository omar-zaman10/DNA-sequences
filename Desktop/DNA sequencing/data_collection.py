from Trellis import Trellis
from channel import channel


c = channel()
T = Trellis()


Pi = 0.1
Pd = 0.1
Ps = 0.3
n = 1000

t,r = c.generate_input_output(n,Pi=Pi,Pd=Pd,Ps=Ps,bits=True)
changes = c.changes

guesses = T.forward_backward(t,r,Pi=Pi,Pd=Pd,Ps=Ps)

i = 0

results = []


for change in changes:
    if change == 'insert': continue

    elif change == 'delete':
        i+=1
        continue

    elif change == 'transmit':
        results.append(guesses[i][0] > 0.5)

    elif change == 'transmit': 
        results.append(guesses[i][1] > 0.5)

    i+=1

print(results.count(True) / len(results))
