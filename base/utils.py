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
        self.vis

    def __enter__(self):
        self.start = time.time()

    def __exit__(self):
        if self.vis:
            print('{}: {} ses'.format(self.name, round(time.time() - self.start, 3))