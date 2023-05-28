import ldpc as ldpc
import numpy as np
import pandas as pd
from Trellis3D import Trellis3D
from channel import channel
from sparsifier import Sparsifier
import time
from pprint import pprint
import multiprocessing
from progress_bar import progress_bar


def overall_decoder(rate,z,k,n,ps,pti,ptd,return_list):

    c = ldpc.code(standard='802.16' ,z=z,rate = rate)
    m = np.random.randint(0,2,c.K) #This is the message


    S = Sparsifier()
    x = c.encode(m) #Codeword
    codeword = ''.join([str(b) for b in x])

    #print(f'Length of codeword {len(codeword)}')




    sparse = S.sparsify(codeword,k,n)


    watermark =  np.random.randint(0,4,len(sparse))

    transmitted = (sparse + watermark) % 4


    bases_mapping = {0:'A', 1:'C', 2:'G', 3:'T'}
    transmitted = [bases_mapping[q] for q  in transmitted]

    #print(f'Length of transmitted {len(transmitted)}')



    C = channel()


    PI = [0.5,0.0,ps]
    PD = [0.0,0.5,ps]
    PS = [pti,ptd,ps]

    recieved = C.bigram_channel(transmitted,PI=PI,PD=PD,PS=PS)


    #print(f'Length of received {len(recieved)}')


    sparse_distribution = S.substitution_distribution(k,n)



    watermark = [bases_mapping[q] for q  in watermark]

    Trellis3d = Trellis3D(sparse_distribution)


    transmitted_likelihoods = Trellis3d.forward_backward(watermark,recieved,PI=PI,PD=PD,PS=PS)

    #pprint(transmitted_likelihoods)

    type1 = 0
    type2 = 0


    for i in range(len(sparse)):

        index_l = transmitted_likelihoods[i]
        decoded = max(index_l,key = lambda x : index_l[x])

        if decoded != transmitted[i]:

            if sparse[i] == 0 : type1 +=1

            else: type2 += 1
    



    codeword_likelihoods = S.decoder(transmitted_likelihoods,watermark,k,n)


    app,it = c.decode(codeword_likelihoods) #Output loglikelihoods




    codeword_estimate = ['0' if a>0 else '1' for a in app  ]
    codeword_estimate = ''.join(codeword_estimate)


    #print(codeword == codeword_estimate)


    o = [a[0] == a[1] for a in zip(codeword,codeword_estimate)]

    m_error = o.count(False) *100.0/ len(o)


    return_list.append((type1*100.0/len(sparse) , type2*100.0/len(sparse) , m_error))

    return type1*100.0/len(sparse) , type2*100.0/len(sparse) , m_error






if __name__ == '__main__':



    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    return_list = manager.list()
    cores = multiprocessing.cpu_count()

    rate = '1/2'
    z = 5
    k,n = 4,5

    ps = 0.02
    pti = 0.02
    ptd = 0.02

    n_points = [i for i in range(3,5)]

    t1_averages = []
    t1_sd = []

    t2_averages = []
    t2_sd = []

    m_averages = []
    m_sd = []

    start = time.time()


    for j,n in enumerate(n_points):    

        return_list[:] = []
        processes = []

        for i in range(cores):
            processes.append(multiprocessing.Process(target=overall_decoder, args=(rate,z,k,n,ps,pti,ptd,return_list)))

        
        for process in processes:
            process.start()

        for process in processes:
            process.join()



        t1_list = [element[0] for element in return_list]
        t2_list = [element[1] for element in return_list]
        m_error_list = [element[2] for element in return_list]

        t1_averages.append(np.mean(t1_list))
        t1_sd.append(np.std(t1_list))

        t2_averages.append(np.mean(t2_list))
        t2_sd.append(np.std(t2_list))

        m_averages.append(np.mean(m_error_list))
        m_sd.append(np.std(m_error_list))

        #print(f't1 average of {np.mean(t1_list)} and standard deviation {np.std(t1_list)} for {t1_list}')
        #print(f't2 average of {np.mean(t2_list)} and standard deviation {np.std(t2_list)} for {t2_list}')
        #print(f'm error average of {np.mean(m_error_list)} for {m_error_list}')

        progress_bar(j+1,len(n_points))

    
    rates = [0.5*k/(2*n) for n in n_points]

    data = pd.DataFrame()

    data['n'] = n_points
    data['t1 average'] = t1_averages
    data['t1 standard deviation'] = t1_sd
    data['t2 average'] = t2_averages
    data['t2 standard deviation'] = t2_sd
    data['m error average'] = m_averages
    data['m standard deviation'] = m_sd
    data['rates'] = rates



    data.to_csv('new_data.csv')

    print(f'Time taken {time.time()-start}s')

