import timeit

UNIT_MILLISECONDS = 'ms'
UNIT_SECONDS = 's'
UNIT_MINUTES = 'm'
UNIT_HOURS = 'h'

time_units = {
    'ms': 1,
    's': 1000,
    'm': 60 * 1000,
    'h': 3600 * 1000
}


class CodeTimer:

    def __init__(
            self,
            name=None,
            silent=False,
            unit=UNIT_MILLISECONDS,
            logger_func=None
    ):
        """
        :param name: A custom name given to a code block
        :param silent: When True, does not print or log any messages
        :param unit: Units to measure time. One of ['ms', 's', 'm', 'h']
        :param logger_func: A function that takes a string parameter
                that is called at the end of the indented block.
                If specified, messages will not be printed to console.
        """

        self.name = name
        self.silent = silent
        self.unit = unit
        self.logger_func = logger_func
        self.log_str = None

    def __enter__(self):
        """
        Start measuring at the start of indent

        :return: CodeTimer object
        """

        self.start = timeit.default_timer()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Stop measuring at the end of indent.
        This will run even if the indented lines raise an exception.
        """

        # Record elapsed time
        self.took = (timeit.default_timer() - self.start) * 1000.0

        # Convert time units
        self.took = self.took / time_units.get(self.unit, time_units['ms'])

        if not self.silent:

            # Craft a log message
            self.log_message = 'Code block{}took: {:.5f} {}'.format(
                str(" '" + self.name + "' ") if self.name else ' ',
                float(self.took),
                str(self.unit))


            if self.logger_func:
                self.logger_func(self.log_message)

            else:
                print(self.log_message)


# function decorator style
def linetimer(
        show_args=False,
        name: str = None,
        silent: bool = False,
        unit: str = UNIT_MILLISECONDS,
        logger_func=None
):
    """
    Decorating a function will log how long it took to execute each function call

    Usage:

    @linetimer()
    def foo():
        pass

    "Code block 'foo()' took xxx ms"

    @linetimer(show_args=True)
    def foo():
        pass

    :param show_args: When True, will print the parameters passed
            into the decorated function
    :param name: If None, uses the name of the function and show_args value.
            Otherwise, same as CodeTimer.
    :param silent: same as CodeTimer
    :param unit: same as CodeTimer
    :param logger_func: same as CodeTimer
    :return: CodeTimer decorated function
    """

    def decorator(func):

        def wrapper(*args, **kwargs):

            if name is None:
                if show_args:
                    block_name = func.__name__ + '('

                    def to_str(val):
                        return [val].__str__()[1:-1]

                    # append args
                    if len(args) > 0:
                        block_name += ', '.join([to_str(arg) for arg in args])

                        if len(kwargs.keys()) > 0:
                            block_name += ', '

                    # append kwargs
                    if len(kwargs.keys()) > 0:
                        block_name += ', '.join([
                            k + '=' + to_str(v) for k, v in kwargs.items()
                        ])

                    block_name += ')'

                else:
                    block_name = func.__name__

            else:
                block_name = name

            with CodeTimer(
                name=block_name,
                silent=silent,
                unit=unit,
                logger_func=logger_func
            ):
                return func(*args, **kwargs)

        return wrapper

    return decorator
