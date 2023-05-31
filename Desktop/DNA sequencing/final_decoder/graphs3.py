import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from stationary import stationary_distribution


data1 = pd.read_csv('Data3/data3_rate_1.csv')



t1_averages1 = data1['t1 average'][1:]
t1_sd1 = data1['t1 standard deviation'][1:]
t2_averages1 = data1['t2 average'][1:]
t2_sd1 = data1['t2 standard deviation'][1:]
m_averages1 = data1['m error average'][1:]
m_sd1 = data1['m standard deviation'][1:]
m_errors1 = data1['m error average'][1:]
m_stds1 = data1['m standard deviation'][1:]

pti_values1 = data1['Probability of Inseertion'][1:]



stationary_values1 = [stationary_distribution(pti,0.02) for pti in pti_values1]

insertion_values = [a[0] for a in stationary_values1]




data2 = pd.read_csv('Data3/data3_rate_3.csv')



t1_averages2 = data2['t1 average'][1:]
t1_sd2 = data2['t1 standard deviation'][1:]
t2_averages2 = data2['t2 average'][1:]
t2_sd2 = data2['t2 standard deviation'][1:]
m_averages2 = data2['m error average'][1:]
m_sd2 = data2['m standard deviation'][1:]
m_errors2 = data2['m error average'][1:]
m_stds2 = data2['m standard deviation'][1:]

pti_values2 = data1['Probability of Inseertion'][1:]




data3 = pd.read_csv('Data3/data3_d_rate_1.csv')



t1_averages3 = data3['t1 average']
t1_sd3 = data3['t1 standard deviation'] 
t2_averages3 = data3['t2 average'] 
t2_sd3 = data3['t2 standard deviation'] 
m_averages3 = data3['m error average'] 
m_sd3 = data3['m standard deviation'] 
m_errors3 = data3['m error average']
m_stds3 = data3['m standard deviation']

ptd_values3 = data3['Probability of Deletions'] 

stationary_values3 = [stationary_distribution(0.02,ptd) for ptd in ptd_values3]

deletion_values = [a[1] for a in stationary_values3]


data4 = pd.read_csv('Data3/data3_d_rate_3.csv')



t1_averages4   = data4['t1 average']
t1_sd4         = data4['t1 standard deviation'] 
t2_averages4   = data4['t2 average'] 
t2_sd4         = data4['t2 standard deviation'] 
m_averages4    = data4['m error average'] 
m_sd4          = data4['m standard deviation'] 
m_errors4      = data4['m error average']
m_stds4        = data4['m standard deviation']

ptd_values4 = data3['Probability of Deletions'] 





#Pi = 0.008
size = len(m_errors1)


y1 = m_errors1
x1 = insertion_values
y1 = np.array(y1)
sd1 = np.array(m_stds1)

y2 = m_errors2
x2 = insertion_values
y2 = np.array(y2)
sd2 = np.array(m_stds2)




y3 = m_errors3
x3 = deletion_values
y3 = np.array(y3)
sd3 = np.array(m_stds3)

y4 = m_errors4
x4 = deletion_values
y4 = np.array(y4)
sd4 = np.array(m_stds4)


y1 /= 100
y2 /= 100

y3 /= 100
y4 /= 100



v_range = 0.0

v_range /= 100

plt.plot(x1,y1,label = 'R = 1/2 Insertions ',color='r')
plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='tomato')

plt.plot(x2,y2,label = 'R = 3/4 Insertions',color='g')
plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='palegreen')


'''

plt.xlabel('Average Rate of Insertions')
plt.ylabel('Overall Error probability')
plt.title('Overall Errors for varying average Insertion rate')

plt.grid()
plt.legend(loc = 'lower right')
plt.show()

'''

plt.plot(x3,y3,label = 'R = 1/2 Deletions',color='b')
plt.fill_between(x3,y3-v_range*sd3,y3+v_range*sd3,color='cornflowerblue')


plt.plot(x4,y4,label = 'R = 3/4 Deletions',color='y')
plt.fill_between(x4,y4-v_range*sd4,y4+v_range*sd4,color='khaki')


plt.xlabel('Stationary Rate')
plt.ylabel('Overall Error probability')
plt.title('Overall Errors for varying average Deletion or Insertion rate')

plt.grid()
plt.legend(loc = 'lower right')
plt.show()


def plot_t12_errors(t1_averages,length,t1_sd,t2_averages,t2_sd,R = '1/2',C = 'Insertion'):


    y1 = np.array(t1_averages)
    x1 = length
    sd1 = np.array(t1_sd)

    y2 = np.array(t2_averages)
    x2 = length
    sd2 = np.array(t2_sd)



    v_range = 0.4

    y1 /= 100
    y2 /= 100
    v_range /= 100


    plt.plot(x1,y1,label = 'Type1 Error',color='b')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='cornflowerblue')

    plt.plot(x2,y2,label = 'Type2 Error',color='y')
    plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='khaki')

    plt.xlabel(f'Average {C} rate')
    plt.ylabel('Error probability')
    plt.title(f'Type1 and Type2 Errors for R = {R} by varying average {C} rate')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()


def plot_t2():


    y1 = np.array(t2_averages1)
    x1 = insertion_values
    sd1 = np.array(t2_sd1)

    y2 = np.array(t2_averages2)
    x2 = insertion_values
    sd2 = np.array(t2_sd2)

    y3 = np.array(t2_averages3)
    x3 = deletion_values
    sd3 = np.array(t2_sd3)

    y4 = np.array(t2_averages4)
    x4 = deletion_values
    sd4 = np.array(t2_sd4)



    v_range = 0.5

    y1/= 100
    y2/= 100
    y3/= 100
    y4/= 100
    v_range/= 100




    plt.plot(x1,y1,label = 'R = 1/2 Insertions',color='r')
    plt.fill_between(x1,y1-v_range*sd1,y1+v_range*sd1,color='tomato')

    plt.plot(x2,y2,label = 'R = 3/4 Insertions',color='g')
    plt.fill_between(x2,y2-v_range*sd2,y2+v_range*sd2,color='palegreen')

    plt.plot(x3,y3,label = 'R = 1/2 Deletions',color='b')
    plt.fill_between(x3,y3-v_range*sd3,y3+v_range*sd3,color='cornflowerblue')

    plt.plot(x4,y4,label = 'R = 3/4 Deletions',color='y')
    plt.fill_between(x4,y4-v_range*sd4,y4+v_range*sd4,color='khaki')


    plt.xlabel('Stationary rate')
    plt.ylabel('Error probability')
    plt.title(f'Type2 Errors for varying average Deletion or Insertion rate')


    plt.grid()
    plt.legend(loc = 'upper left')
    plt.show()

def plot_t1():


    y1 = np.array(t1_averages1)
    x1 = insertion_values
    sd1 = np.array(t1_sd1)

    y2 = np.array(t1_averages2)
    x2 = insertion_values
    sd2 = np.array(t1_sd2)

    y3 = np.array(t1_averages3)
    x3 = deletion_values
    sd3 = np.array(t1_sd3)

    y4 = np.array(t1_averages4)
    x4 = deletion_values
    sd4 = np.array(t1_sd4)



    v_range = 0.01




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

#plot_t12_errors(t1_averages1,insertion_values,t1_sd1,t2_averages1,t2_sd1,R = '1/2')

#plot_t12_errors(t1_averages2,insertion_values,t1_sd2,t2_averages2,t2_sd2,R = '3/4')

#plot_t12_errors(t1_averages3,deletion_values,t1_sd3,t2_averages3,t2_sd3,R = '1/2',C='Deletion')

#plot_t12_errors(t1_averages4,deletion_values,t1_sd4,t2_averages4,t2_sd4,R = '3/4',C='Deletion')

plot_t2()
#plot_t1()


#plot_t12_errors(t1_averages1,rates3,t1_sd1,t1_averages3,t1_sd3,R = '3/4')
