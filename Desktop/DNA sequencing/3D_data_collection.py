from Trellis3D import Trellis3D
#from Trellis import Trellis
from channel import channel
import multiprocessing
import pandas as pd
import numpy as np
import time
from progress_bar import progress_bar


#c = channel()
#T = Trellis()
#T3D = Trellis3D()

def run(n,PI,PD,PS,return_list):
    C= channel()
    T3D = Trellis3D()
    transmitted,recieved = C.generate_bigram_input_output(n,PI=PI,PD=PD,PS=PS)
    changes = C.changes
    likelihoods = T3D.forward_backward(transmitted,recieved,PI=PI,PD=PD,PS=PS)
    predictions = []

    i,j = 0,0

    for change in changes:

        if change == 'insert':
            j+=1
            
        elif change == 'transmit' or change == 'substitute':

            p = likelihoods[i]
            symbol = recieved[j]
            symbol_hat = max(p,key = lambda x: p[x])
            #print(f'likeilihood distribution {p} and estimated symbol {symbol_hat}')
            predictions.append(symbol_hat==symbol)
            i+=1
            j+=1
            pass
        elif change == 'delete':
            p = likelihoods[i]
            if j == len(recieved) : continue
            symbol = recieved[j]
            symbol_hat = max(p,key = lambda x: p[x])
            #print(f'likeilihood distribution {p} and estimated symbol {symbol_hat}')
            predictions.append(symbol_hat==symbol)

            i+=1
            #For now pass but later implement changes for deletion
            pass


    deletions = changes.count('delete') *100.0/ len(predictions)

    errors = predictions.count(False) *100.0/ len(predictions)

    return_list.append(errors)


if __name__ == '__main__':



    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    return_list = manager.list()
    cores = multiprocessing.cpu_count()



    n = 500 #Change n to 1000
    points = 5 

    Ps_values = np.linspace(0,0.2,points)
    Pid_values = [0.005,0.01,0.02]
    data_dict = {'Ps':[],'Pi':[],'Pd':[],"Average error":[],"SD":[]}

    

    counter = 0
    total = points*len(Pid_values)
    start = time.time()
    print(total)

    for p in Pid_values:
        Pi,Pd =p,p
        
        for Ps in Ps_values:
            return_list[:] = []

            PI = [0.5,Pd,Ps]  # Distribution Pi, Pd,Ps Pt = 0.3
            PD = [Pi,0.5,Ps]  # Should it still be Ps ???
            PS = [Pi,Pd,Ps]
            
            processes = []
            for i in range(cores):
                #print('registering process %d' % i)
                processes.append(multiprocessing.Process(target=run, args=(n,PI,PD,PS,return_list)))

            
            for process in processes:
                process.start()

            for process in processes:
                process.join()
            end = time.time()

            avg  = np.mean(return_list)
            sd = np.std(return_list)
            print(return_list)
            print(f'average {avg} std {sd}')
            data_dict['Average error'].append(avg)
            data_dict["SD"].append(sd)
            data_dict['Ps'].append(Ps)
            data_dict['Pd'].append(Pd)
            data_dict['Pi'].append(Pi)
            
            print('-'*165)

    

  



    df = pd.DataFrame.from_dict(data_dict)

    df.to_csv('3D_TESTING.csv')


    end = time.time()
    print(f'Time taken {end-start}s for n = {n}, repeats = {cores}, points = {points}')
    print(f'Time taken per trellis run {(end-start)/(total*cores)}')