import multiprocessing
import time

start = time.time()

def do():
    global r1
    output = []
    n = 1_000_000
    for i in range(n):
        
        output.append(i**2)

    r1.append(output)
    return 


def do1():
    global r2
    output = []
    n = 1_000_000
    for i in range(n):
        
        output.append(i**2)

    r2.append(output)
    return 


cores = multiprocessing.cpu_count()

r1 = []
r2 = []


if __name__ == '__main__':
    start = time.time()

    processes = []

    for i in range(cores):
        print('registering process %d' % i)
        processes.append(multiprocessing.Process(target=do))


    for process in processes:
        process.start()

    for process in processes:
        process.join()
    end = time.time()
    print(f'Time taken for multiprocessing was {end - start}s')




    start = time.time()
    for i in range(cores):
        do1()

    end = time.time()
    print(f'Time taken was {end - start}s')
    print(r1==r2)
