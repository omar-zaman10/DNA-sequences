import multiprocessing
import time

start = time.time()

def do(index,return_dict):
    global r1
    output = []
    n = 1_000_000
    for i in range(n):
        
        output.append(i**2)

    r1.append(output)
    #return 'hello world'
    return_dict[index] = f'hello world {index}'

def do1():
    global r2
    output = []
    n = 1_000_000
    for i in range(n):
        
        output.append(i**2)

    r2.append(output)
    return 'hello'


cores = multiprocessing.cpu_count()

r1 = []
r2 = []


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    start = time.time()

    processes = []

    for i in range(cores):
        print('registering process %d' % i)
        processes.append(multiprocessing.Process(target=do, args=(i,return_dict)))


    for process in processes:
        process.start()

    for process in processes:
        process.join()
    end = time.time()
    print(f'Time taken for multiprocessing was {end - start}s')

    print(return_dict)


    start = time.time()
    for i in range(cores):
        do1()

    end = time.time()
    print(f'Time taken was {end - start}s')
    print(len(r2[0]))