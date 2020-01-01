import os
import time

class Timer():
    
    '''
    Usage:
        IMPLEMENTATION:
        with Timer(NAME) as t:
            # CODES TO BE TIMED

        OUTPUT:
        NAME: TIME sec
    '''
    def __init__(self, name, vis=True):

        self.name = name
        self.vis = vis
        print('working on {} ... '.format(name), end='')

    def __enter__(self):

        self.start = time.time()

    def __exit__(self, *args):

        if self.vis:
            interval = time.time() - self.start
            if interval > 1:
                print('done. {} s'.format(round(interval, 2)))
            else:
                print('done. {} ms'.format(round(interval * 1000, 2)))

class Cprinter():

    '''
    Usage:
        print something to cli with color
    '''
    def __init__(self):

        self.id2color = {'system': '\x1b[4;30;47m*\x1b[0m'}
        self.colors = {'\x1b[6;0;{}m*\x1b[0m'.format(x) for x in range(40, 47)}.union(
            {'\x1b[6;30;47m*\x1b[0m'}
        )

    def __call__(self, data, id=None, end='\n'):

        if 'owner' in dir(data):
            name = data.owner
        elif 'name' in dir(data):
            name = data.name
        else:
            name = id
        if name == None:
            print(data, end=end)
        else:
            if not name in self.id2color.keys():
                self.id2color[name] = self.colors.pop()
            print(self.id2color[name].replace('*', str(data)), end=end)

cprint = Cprinter()

def error_filter(func, *args):

    '''
    Usage:
        a wrapper for codes that may trigger errors for no reason
    '''
    while True:
        try:
            tmp = func(*args)
        except:
            pass
        else:
            return tmp

def clear():

    os.system('cls' if os.name == 'nt' else 'clear')