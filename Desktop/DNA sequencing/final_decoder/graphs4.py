import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv('Data4/rate_1.csv')



t1_averages1 = data1['t1 average']
t1_sd1 = data1['t1 standard deviation'] 
t2_averages1 = data1['t2 average'] 
t2_sd1 = data1['t2 standard deviation'] 
m_averages1 = data1['m error average'] 
m_sd1 = data1['m standard deviation'] 
m_errors1 = data1['m error average']
m_stds1 = data1['m standard deviation']
ps_values1 = data1['Probability of substitution']




data2 = pd.read_csv('Data4/rate_3.csv')



t1_averages2 = data2['t1 average']
t1_sd2 = data2['t1 standard deviation'] 
t2_averages2 = data2['t2 average'] 
t2_sd2 = data2['t2 standard deviation'] 
m_averages2 = data2['m error average'] 
m_sd2 = data2['m standard deviation'] 
m_errors2 = data2['m error average']
m_stds2 = data2['m standard deviation']
ps_values2 = data2['Probability of substitution']




#Pi = 0.008
size = len(m_errors1)


y1 = m_errors1
x1 = ps_values1
y1 = np.array(y1)
sd1 = np.array(m_stds1)

y2 = m_errors2
x2 = ps_values2
y2 = np.array(y2)
sd2 = np.array(m_stds2)




v_range = 1

plt.plot(x1,y1,label = 'R = 1/2',color='b')
plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

plt.plot(x2,y2,label = 'R = 3/4',color='r')
plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='tomato')



plt.xlabel('Probability of Substitution')
plt.ylabel('Overall Decoding Error probability %')
plt.title('Decoding Errors for Probability of substitutions')

plt.grid()
plt.legend(loc = 'lower right')
plt.show()


def plot_t12_errors(t1_averages,length,t1_sd,t2_averages,t2_sd,R = '1/2'):


    y1 = np.array(t1_averages)
    x1 = length
    sd1 = np.array(t1_sd)

    y2 = np.array(t2_averages)
    x2 = length
    sd2 = np.array(t2_sd)



    v_range = 0.4




    plt.plot(x1,y1,label = 'Type1 Error',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

    plt.plot(x2,y2,label = 'Type2 Error',color='y')
    plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='khaki')

    plt.xlabel('Overall Rates')
    plt.ylabel('Error percentage %')
    plt.title(f'Type1 and Type2 Errors for R = {R}')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()


def plot_t2():


    y1 = np.array(t2_averages1)
    x1 = ps_values1
    sd1 = np.array(t2_sd1)

    y2 = np.array(t2_averages2)
    x2 = ps_values2
    sd2 = np.array(t2_sd2)




    v_range = 1




    plt.plot(x1,y1,label = 'R = 1/2',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

    plt.plot(x2,y2,label = 'R = 2/3',color='g')
    plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='palegreen')

 


    plt.xlabel('Overall Rates')
    plt.ylabel('Error percentage %')
    plt.title(f'Type2 Errors for different ldpc code rates')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()

def plot_t1():


    y1 = np.array(t1_averages1)
    x1 = ps_values1
    sd1 = np.array(t1_sd1)

    y2 = np.array(t1_averages2)
    x2 = ps_values2
    sd2 = np.array(t1_sd2)




    v_range = 0.3




    plt.plot(x1,y1,label = 'R = 1/2',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

    plt.plot(x2,y2,label = 'R = 2/3',color='y')
    plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='khaki')



    plt.xlabel('Overall Rates')
    plt.ylabel('Error percentage %')
    plt.title(f'Type1 Errors for different ldpc code rates')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()

plot_t12_errors(t1_averages1,ps_values1,t1_sd1,t2_averages1,t2_sd1,R = '1/2')
plot_t12_errors(t1_averages2,ps_values1,t1_sd2,t2_averages2,t2_sd2,R = '3/4')

plot_t2()
plot_t1()


#plot_t12_errors(t1_averages1,rates3,t1_sd1,t1_averages3,t1_sd3,R = '3/4')
