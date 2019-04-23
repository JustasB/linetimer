import timeit

class CodeTimer:

    def __init__(self, name=None):
        '''Allows giving indented blocks their own name. Blank by default'''
        self.name = name

    def __enter__(self):
        '''Start measuring at the start of indent'''
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        '''
            Stop measuring at the end of indent. This will run even 
            if the indented lines raise an exception.
        '''
        self.took = (timeit.default_timer() - self.start) * 1000.0
        print('Code block' + 
              (" '"  + str(self.name) + "'" if self.name else '') + 
              ' took: ' + str(self.took) + ' ms')
