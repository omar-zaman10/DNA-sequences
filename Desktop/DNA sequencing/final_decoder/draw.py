import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv('Data1/data_rate_1.csv')



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
#lengths = data1['codeword_length']




data2 = pd.read_csv('Data1/data_rate_2.csv')



t1_averages2 = data2['t1 average']
t1_sd2 = data2['t1 standard deviation'] 
t2_averages2 = data2['t2 average'] 
t2_sd2 = data2['t2 standard deviation'] 
m_averages2 = data2['m error average'] 
m_sd2 = data2['m standard deviation'] 
n_points2 = data2['n'] 
m_errors2 = data2['m error average']
m_stds2 = data2['m standard deviation']
rates2 = data2['rates']



data3 = pd.read_csv('Data1/data_rate_3.csv')



t1_averages3 = data3['t1 average']
t1_sd3 = data3['t1 standard deviation'] 
t2_averages3 = data3['t2 average'] 
t2_sd3 = data3['t2 standard deviation'] 
m_averages3 = data3['m error average'] 
m_sd3 = data3['m standard deviation'] 
n_points3 = data3['n'] 
m_errors3 = data3['m error average']
m_stds3 = data3['m standard deviation']
rates3 = data3['rates']


data4 = pd.read_csv('Data1/data_rate_5.csv')



t1_averages4   = data4['t1 average']
t1_sd4         = data4['t1 standard deviation'] 
t2_averages4   = data4['t2 average'] 
t2_sd4         = data4['t2 standard deviation'] 
m_averages4    = data4['m error average'] 
m_sd4          = data4['m standard deviation'] 
n_points4      = data4['n'] 
m_errors4      = data4['m error average']
m_stds4        = data4['m standard deviation']
rates4         = data4['rates']



#Pi = 0.008
size = len(m_errors1)


y1 = m_errors1
x1 = rates1
y1 = np.array(y1)
sd1 = np.array(m_stds1)

y2 = m_errors2
x2 = rates2
y2 = np.array(y2)
sd2 = np.array(m_stds2)




y3 = m_errors3
x3 = rates3
y3 = np.array(y3)
sd3 = np.array(m_stds3)

y4 = m_errors4
x4 = rates4
y4 = np.array(y4)
sd4 = np.array(m_stds4)


y1 /= 100
y2 /= 100
y3 /= 100
y4 /= 100



v_range = 0

plt.plot(x1,y1,label = 'R = 1/2',color='b')
plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

plt.plot(x2,y2,label = 'R = 2/3',color='y')
plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='khaki')

plt.plot(x3,y3,label = 'R = 3/4',color='r')
plt.fill_between(x3,y3-v_range*sd3,y3+v_range*sd3,color='tomato')


plt.plot(x4,y4,label = 'R = 5/6',color='g')
plt.fill_between(x4,y4-v_range*sd4,y4+v_range*sd4,color='palegreen')


plt.xlabel('Overall Rate')
plt.ylabel('Overall Error probability ')
plt.title('Overall Errors for different LDPC Rates')

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

    y2 /= 100
    y1 /= 100


    v_range = 0.4

    v_range /= 100



    plt.plot(x1,y1,label = 'Type1 Error',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

    plt.plot(x2,y2,label = 'Type2 Error',color='y')
    plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='khaki')

    plt.xlabel('Overall Rate')
    plt.ylabel('Probability of Error')
    plt.title(f'Type1 and Type2 Errors for R = {R}')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()


def plot_t2():


    y1 = np.array(t2_averages1)
    x1 = rates1
    sd1 = np.array(t2_sd1)

    y2 = np.array(t2_averages2)
    x2 = rates2
    sd2 = np.array(t2_sd2)

    y3 = np.array(t2_averages3)
    x3 = rates3
    sd3 = np.array(t2_sd3)

    y4 = np.array(t2_averages4)
    x4 = rates4
    sd4 = np.array(t2_sd4)



    v_range = 0.3

    y1/= 100
    y2/= 100
    y3/= 100
    y4/= 100

    v_range /= 100




    plt.plot(x1,y1,label = 'R = 1/2',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

    plt.plot(x2,y2,label = 'R = 2/3',color='y')
    plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='khaki')

    plt.plot(x3,y3,label = 'R = 3/4',color='r')
    plt.fill_between(x3,y3-v_range*sd3,y3+v_range*sd3,color='tomato')

    plt.plot(x4,y4,label = 'R = 5/6',color='g')
    plt.fill_between(x4,y4-v_range*sd4,y4+v_range*sd4,color='lightgreen')


    plt.xlabel('Overall Rate')
    plt.ylabel('Probability of Error')
    plt.title(f'Type2 Errors for different ldpc code rates')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()

def plot_t1():


    y1 = np.array(t1_averages1)
    x1 = rates1
    sd1 = np.array(t1_sd1)

    y2 = np.array(t1_averages2)
    x2 = rates2
    sd2 = np.array(t1_sd2)

    y3 = np.array(t1_averages3)
    x3 = rates3
    sd3 = np.array(t1_sd3)

    y4 = np.array(t1_averages4)
    x4 = rates4
    sd4 = np.array(t1_sd4)



    v_range = 0.05




    plt.plot(x1,y1,label = 'R = 1/2',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

    plt.plot(x2,y2,label = 'R = 2/3',color='y')
    plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='khaki')

    plt.plot(x3,y3,label = 'R = 3/4',color='r')
    plt.fill_between(x3,y3-v_range*sd3,y3+v_range*sd3,color='tomato')

    plt.plot(x4,y4,label = 'R = 5/6',color='g')
    plt.fill_between(x4,y4-v_range*sd4,y4+v_range*sd4,color='lightgreen')


    plt.xlabel('Overall Rates')
    plt.ylabel('Error percentage %')
    plt.title(f'Type1 Errors for different ldpc code rates')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()

plot_t12_errors(t1_averages1,rates1,t1_sd1,t2_averages1,t2_sd1,R = '1/2')
plot_t12_errors(t1_averages2,rates2,t1_sd2,t2_averages2,t2_sd2,R = '2/3')
plot_t12_errors(t1_averages3,rates3,t1_sd3,t2_averages3,t2_sd3,R = '3/4')

plot_t12_errors(t1_averages4,rates4,t1_sd4,t2_averages4,t2_sd4,R = '5/6')
plot_t2()
plot_t1()


#plot_t12_errors(t1_averages1,rates3,t1_sd1,t1_averages3,t1_sd3,R = '3/4')