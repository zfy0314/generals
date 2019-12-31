import time

class Timer():
    
    '''
    Usage:
        IMPLEMENTATION:
        with Timer(NAME) as t:
            # CODES TO BE TIMED

        OUTPUT:
        NAME: TIME sec

        set vis=False to close debug
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