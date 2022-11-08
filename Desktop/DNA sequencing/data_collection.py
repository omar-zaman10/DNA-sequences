from Trellis import Trellis
from channel import channel
import numpy as np
import pandas as pd
import time


c = channel()
T = Trellis()

start = time.time()




n = 1000 #Change n to 1000
repeats = 25
points = 10

Ps_values = np.linspace(0,0.2,points)
data_dict = {'Ps':[],'Pi':[],'Pd':[],"Average error":[],"SD":[]}

counter = 1

def run():
    global counter
    for Ps in Ps_values:
        percentage = []
        data_dict['Ps'].append(Ps)
        data_dict['Pd'].append(Pd)
        data_dict['Pi'].append(Pi)


        for _ in range(repeats):



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

            count = results.count(False) *100.0/ len(results)
            percentage.append(count)
            print(counter, round(counter *100.0/ (points*3*repeats),2),' percent')
            counter +=1

        percentage = np.array(percentage)
        avg  = np.mean(percentage)
        sd = np.std(percentage)

        data_dict['Average error'].append(avg)
        data_dict["SD"].append(sd)

        print(avg,'Average')
        


Pi = 0.008
Pd = 0.008
run()


Pi = 0.01
Pd = 0.01
run()


Pi = 0.02
Pd = 0.02
run()



df = pd.DataFrame.from_dict(data_dict)

df.to_csv('n=1000_r=25.csv')

end = time.time()
print(f'Time taken for n = {n}, repeats = {repeats} {end-start}s')