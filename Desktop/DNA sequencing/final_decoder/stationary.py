import numpy as np

def stationary_distribution(pti,ptd,pii=0.5,pid=0,pdi=0,pdd=0.5):
    ptt = 1 - pti - ptd
    pit = 1 - pii - pid
    pdt = 1 - pdi - pdd

    PI = np.array([pii,pid,pit])
    PD = np.array([pdi,pdd,pdt])
    PT = np.array([pti,ptd,ptt])

    P = np.matrix([PI,PD,PT]).T


    w,v = np.linalg.eig(P)

    v = np.array(v)

    s = np.array([e[0] for e in v])


    s /= sum(s)

    return s


if __name__ == '__main__':

    s = stationary_distribution(0.13,0.02)

    print(s)