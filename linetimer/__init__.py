import timeit
from typing import Union, Optional

UNIT_NANOSECONDS = 'ns'
UNIT_MICROSECONDS = 'us'
UNIT_MILLISECONDS = 'ms'
UNIT_SECONDS = 's'
UNIT_MINUTES = 'm'
UNIT_HOURS = 'h'

time_units = {
    UNIT_NANOSECONDS: 1/1000000,
    UNIT_MICROSECONDS: 1/1000,
    UNIT_MILLISECONDS: 1,
    UNIT_SECONDS: 1000,
    UNIT_MINUTES: 60 * 1000,
    UNIT_HOURS: 3600 * 1000
}


class CodeTimer:

    def __init__(
            self,
            name: str = None,
            silent: bool = False,
            unit: str = UNIT_MILLISECONDS,
            logger_func=None,
            threshold: Optional[Union[int, float]] = None
    ):
        """
        :param name: A custom name given to a code block
        :param silent: When True, does not print or log any messages
        :param unit: Units to measure time.
                One of ['ns', 'us', 'ms', 's', 'm', 'h']
        :param logger_func: A function that takes a string parameter
                that is called at the end of the indented block.
                If specified, messages will not be printed to console.
        :param threshold: A integer or float value. If time taken by code block
                took greater than or equal value, only then log.
                If None, will bypass this parameter.
        """

        self.name = name
        self.silent = silent
        self.unit = unit if unit else UNIT_MILLISECONDS
        self.logger_func = logger_func
        self.log_str = None
        self.threshold = threshold

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

        # Record elapsed time in milliseconds (seconds * 1000 = milliseconds)
        self.took = (timeit.default_timer() - self.start) * 1000.0

        # Convert time into given units
        self.took = (
                self.took
                / time_units.get(self.unit, time_units[UNIT_MILLISECONDS])
        )

        if not self.silent and (
                not self.threshold or self.took <= self.threshold
        ):

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
        logger_func=None,
        threshold: Optional[Union[int, float]] = None
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
    :param silent: When True, does not print or log any messages
    :param unit: Units to measure time. One of ['ns', 'us', 'ms', 's', 'm', 'h']
    :param logger_func: A function that takes a string parameter
                that is called at the end of the indented block.
                If specified, messages will not be printed to console.
    :param threshold: A integer or float value. If time taken by code block
                took greater than or equal value, only then log.
                If None, will bypass this parameter.
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
                logger_func=logger_func,
                threshold=threshold
            ):
                return func(*args, **kwargs)

        return wrapper

    return decorator
