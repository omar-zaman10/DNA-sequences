import colorama
import time

def progress_bar(progress,total,color=colorama.Fore.RED):

    percent = 100.0*progress/total

    bar = '█' *int(percent) + '-'*(100-int(percent))
    print(color + f'\r|{bar}| {percent:.2f}%',end = '\r')
    
    if progress == total:
        print(colorama.Fore.GREEN + f'\r|{bar}| {percent:.2f}%',end = '\r')
        print('')
        print(colorama.Fore.RESET)


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()



if __name__ == '__main__':

    print(colorama.Fore.RESET)
    start = time.time()

    for i in range(1,1_000_01):
        progress_bar(i,1_000_00)



    print('end')
    print(f'Time taken {time.time() - start}')