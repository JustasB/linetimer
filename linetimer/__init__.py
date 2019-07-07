import timeit

time_units = {'ms': 1, 's': 1000, 'm': 60 * 1000, 'h': 3600 * 1000}


class CodeTimer:

    def __init__(self, name=None, silent=False, unit='ms', logger_func=None):
        """Allows giving indented blocks their own name. Blank by default"""
        self.name = name
        self.silent = silent
        self.unit = unit
        self.logger_func = logger_func

    def __enter__(self):
        """Start measuring at the start of indent"""
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        """
            Stop measuring at the end of indent. This will run even
            if the indented lines raise an exception.
        """
        self.took = (timeit.default_timer() - self.start) * 1000.0
        self.took = self.took / time_units.get(self.unit, time_units['ms'])

        if not self.silent:
            log_str = 'Code block{}took: {:.5f} {}'.format(
                str(" '" + self.name + "' ") if self.name else ' ',
                float(self.took),
                str(self.unit))

            if self.logger_func:
                self.logger_func(log_str)
            else:
                print(log_str)
