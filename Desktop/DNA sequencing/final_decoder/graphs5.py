import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv('Data5/data5_rate1.csv')


'''
Varying k for a fixed k:n ratio and seeing how the errors change
'''



t1_averages1 = data1['t1 average']
t1_sd1 = data1['t1 standard deviation'] 
t2_averages1 = data1['t2 average'] 
t2_sd1 = data1['t2 standard deviation'] 
m_averages1 = data1['m error average'] 
m_sd1 = data1['m standard deviation'] 
n_points1 = data1['n'] 
m_errors1 = data1['m error average']
m_stds1 = data1['m standard deviation']
rates1 = data1['rates']

print(rates1)


#Pi = 0.008
size = len(m_errors1)


y1 = m_errors1
x1 = n_points1
y1 = np.array(y1)
sd1 = np.array(m_stds1)



y1 /= 100




v_range = 0.4

v_range /= 100


plt.plot(x1,y1,label = 'R = 1/2',color='g')
plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='palegreen')




plt.xlabel('k=n')
plt.ylabel('Overall Error probability %')
plt.title('Overall Error for varying k,n values')

plt.grid()
plt.legend(loc = 'lower right')
plt.show()


def plot_t12_errors(t1_averages,rates,t1_sd,t2_averages,t2_sd,R = '1/2'):


    y1 = np.array(t1_averages)
    x1 = rates
    sd1 = np.array(t1_sd)

    y2 = np.array(t2_averages)
    x2 = rates
    sd2 = np.array(t2_sd)

    y1 /= 100
    y2 /= 100

    v_range = 0.4

    v_range /= 100




    plt.plot(x1,y1,label = 'Type1 Error',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

    plt.plot(x2,y2,label = 'Type2 Error',color='y')
    plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='khaki')

    plt.xlabel('k=n')
    plt.ylabel('Error probability')
    plt.title(f'Type1 and Type2 Errors for R = {R}')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()


def plot_t2():


    y1 = np.array(t2_averages1)
    x1 = rates1
    sd1 = np.array(t2_sd1)

    



    v_range = 0.2




    plt.plot(x1,y1,label = 'R = 1/2',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')


    plt.xlabel('Overall Rates')
    plt.ylabel('Error percentage %')
    plt.title(f'Type2 Errors for different ldpc code rates')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()

def plot_t1():


    y1 = np.array(t1_averages1)
    x1 = rates1
    sd1 = np.array(t1_sd1)




    v_range = 0.05




    plt.plot(x1,y1,label = 'R = 1/2',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')



    plt.xlabel('Overall Rates')
    plt.ylabel('Error percentage %')
    plt.title(f'Type1 Errors for different ldpc code rates')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()

plot_t12_errors(t1_averages1,n_points1,t1_sd1,t2_averages1,t2_sd1,R = '1/2')


#plot_t12_errors(t1_averages2,rates2,t1_sd2,t2_averages2,t2_sd2,R = '2/3')
#plot_t12_errors(t1_averages3,rates3,t1_sd3,t2_averages3,t2_sd3,R = '3/4')

#plot_t12_errors(t1_averages4,rates4,t1_sd4,t2_averages4,t2_sd4,R = '5/6')
#plot_t2()
#plot_t1()


#plot_t12_errors(t1_averages1,rates3,t1_sd1,t1_averages3,t1_sd3,R = '3/4')