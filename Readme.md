[![Build Status](https://travis-ci.com/JustasB/linetimer.svg?branch=master)](https://travis-ci.com/JustasB/linetimer)
[![codecov](https://codecov.io/gh/JustasB/linetimer/branch/master/graph/badge.svg)](https://codecov.io/gh/JustasB/linetimer)
[![PyPI version](https://badge.fury.io/py/linetimer.svg)](https://badge.fury.io/py/linetimer)

# linetimer: A small Python class to measure the time taken by indented lines.

[linetimer](https://pypi.org/project/linetimer/) is a small Python class to quickly measure the time taken by a block of indented lines

# Installation

To install the library, simply type in `pip install linetimer` in your terminal.

# Usage

The basic usage is:

```
from linetimer import CodeTimer

with CodeTimer():
   line_to_measure()
   another_line()
   # etc...
```

Which will show the following after the indented line(s) finishes executing:

```
Code block took: x.xxx ms
```

You can also **name the code blocks** you want to measure:

```
with CodeTimer('loop 1'):
   for i in range(100000):
      pass

with CodeTimer('loop 2'):
   for i in range(100000):
      pass

Code block 'loop 1' took: 4.991 ms
Code block 'loop 2' took: 3.666 ms
```

And **nest** them:

```
with CodeTimer('Outer'):
   for i in range(100000):
      pass

   with CodeTimer('Inner'):
      for i in range(100000):
         pass

   for i in range(100000):
      pass

Code block 'Inner' took: 2.382 ms
Code block 'Outer' took: 10.466 ms
```

To **get the time taken in different units**, use the `unit` parameter:
```
with CodeTimer('Block', unit='h'):
   slow_function()
   
Code block 'Block' took: 2.382 h
```

Supported units are ns, us, ms, s , m, h corresponding to nanoseconds, microseconds, milliseconds, seconds, minutes, hours.

If you need to **retain the time taken**, you can do it with:
```
ct = CodeTimer()

with ct:
   slow_function()
   
ct.took # This contains the time taken as per the unit provided (milliseconds by default)
```

Sometimes you want to **use your own dedicated logger**, you can do it with:
```
import logging
my_logger = logging.get_logger('xyz')

with CodeTimer('Block', unit='h', logger_func = my_logger.info):
   slow_function()
```
This will log to an appropriate handler,
```
INFO - Code block 'Block' took: 2.382 h
```

If you need to **turn off the printed statements**, use the `silent=True` argument

```
with CodeTimer(silent=True):
   slow_function()
   
# There will be no printed output
```

You can also use **function decorator** syntax, like this:

```
from linetimer import linetimer

@linetimer()
def my_function(a, b):
   pass

my_function('a', 'b')

>>> Code block 'my_function' took x.yz ms

@linetimer(show_args=True) # will print function parameters
def my_function(a, b):
   pass

my_function('a', b='b')

>>> Code block 'my_function('a', b='b') took x.yz ms

```

Now you can add threshold to log only necessary statements, which have execution
time greater than equal to given threshold value.

By default, threshold is set to 'None', i.e., no threshold.

Threshold value is set in specified unit.
For e.g., To set threshold value to 1 second, 
- unit='ns' => threshold=1000000000
- unit='us' => threshold=1000000
- unit='ms' => threshold=1000
- unit='s' => threshold=1
- unit='m' => threshold=1/60
- unit='h' => threshold=1/3600
```
from linetimer import linetimer

@linetimer(threshold=None)
def my_function():
   pass

my_function()

>>> Code block 'my_function' took x.yz ms

@linetimer(threshold=1000) # will log only when execution time is >= 1000 milliseconds
def my_function():
   pass

my_function()

>>> Code block 'my_function' took x.yz ms

@linetimer(unit='us', threshold=1000) # will log only when execution time is >= 1000 microseconds
def my_function():
   pass

my_function()

>>> Code block 'my_function' took x.yz us

@linetimer(unit='ns', threshold=1000) # will log only when execution time is >= 1000 nanoseconds
def my_function():
   pass

my_function()

>>> Code block 'my_function' took x.yz ns

```

If you like this package, [upvote it on StackOverflow](https://stackoverflow.com/a/52749808/407108).

# Issues
If you encounter a problem, create an [issue on Github](https://github.com/JustasB/linetimer/issues).

# Contributing
To contribute, please [open an issue](https://github.com/JustasB/linetimer/issues) first and discuss your plan for contributing. Then fork this repository and commit [a pull-request](https://help.github.com/en/articles/about-pull-requests) with your changes.

