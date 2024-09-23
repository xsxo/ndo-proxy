from sys import argv
from platform import system
from subprocess import call
from random import randint

clear = lambda: call('cls' if system() == 'Windows' else 'clear', shell=True)

def ar():
    ar_var = argv[1:]

    if len(ar_var) >= 2:
        try:
            host = ar_var[0]
            port = int(ar_var[1])
            return host, port
        except:
            pass

    elif len(ar_var) == 1:
        try:
            if ar_var[0].__contains__(':'):
                host, port = ar_var[0].split(':')
                port = int(port)
            else:
                host = ar_var[0]
                port = randint(1000, 8995)
            return host, port
        except:
            pass
            
    while 1:
        try:
            host = input('- ip: ')
            port = int(input('- port: '))
            break
        except:
            clear()
            print('- somthing happned please try again...')
    return host, port