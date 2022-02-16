from time import sleep


def test_single_blank():
    from linetimer import CodeTimer

    ct = CodeTimer()

    with ct:
        sleep(0.1)

    assert ct.took >= 100.0


def test_single_named():
    from linetimer import CodeTimer

    name = "name"

    ct = CodeTimer(name)

    with ct:
        sleep(0.1)

    assert ct.took >= 100.0
    assert ct.name == name


def test_two_named():
    from linetimer import CodeTimer

    name1 = "name1"
    name2 = "name2"

    ct1 = CodeTimer(name1)

    with ct1:
        sleep(0.1)

    ct2 = CodeTimer(name2)

    with ct2:
        sleep(0.2)

    assert ct1.took >= 100.0
    assert ct1.name == name1

    assert ct2.took >= 200.0
    assert ct2.name == name2


def test_two_nested():
    from linetimer import CodeTimer

    name1 = "outer"
    name2 = "inner"

    ct1 = CodeTimer(name1)

    with ct1:
        sleep(0.1)

        ct2 = CodeTimer(name2)

        with ct2:
            sleep(0.2)

    assert ct1.took >= 300.0
    assert ct1.name == name1

    assert ct2.took >= 200.0
    assert ct2.name == name2


def test_time_unit():
    from linetimer import CodeTimer

    unit1 = 's'

    ct1 = CodeTimer('ct_' + unit1, unit=unit1)

    with ct1:
        sleep(0.1)

    assert ct1.took >= 0.1
    assert ct1.unit == unit1

    unit2 = 'xyz'

    ct2 = CodeTimer('ct_' + unit2, unit=unit2)

    with ct2:
        sleep(0.1)

    assert ct2.took >= 100
    assert ct2.unit == unit2


def test_logger_func(capsys):
    import logging.config
    from linetimer import CodeTimer

    logger_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(levelname)s] - %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': True
            }
        }
    }

    logging.config.dictConfig(logger_config)

    logger = logging.getLogger()

    with CodeTimer('ct', unit='s', logger_func=logger.info):
        sleep(0.1)

    captured = capsys.readouterr()
    assert captured.out.startswith("[INFO] - Code block 'ct' took: 0.1")
    assert captured.out.endswith(' s\n')


def test_codetimer_with_unit_as_microseconds(capsys):
    from linetimer import CodeTimer

    name = "name"

    ct = CodeTimer(name, unit='us')

    with ct:
        sleep(0.11)

    assert ct.took >= 100000.0
    assert ct.name == name


def test_codetimer_with_unit_as_nanoseconds(capsys):
    from linetimer import CodeTimer

    name = "name"

    ct = CodeTimer(name, unit='ns')

    with ct:
        sleep(0.11)

    assert ct.took >= 100000000.0
    assert ct.name == name


def test_codetimer_with_threshold_in_microseconds_logs_message(capsys):
    from linetimer import CodeTimer

    name = "name"

    ct = CodeTimer(name, unit='us', threshold=100000)

    with ct:
        sleep(0.11)

    assert ct.took >= 100000.0
    assert ct.name == name
    assert ct.log_message.strip()


def test_codetimer_with_threshold_in_nanoseconds_logs_message(capsys):
    from linetimer import CodeTimer

    name = "name"

    ct = CodeTimer(name, unit='ns', threshold=100000000)

    with ct:
        sleep(0.11)

    assert ct.took >= 100000000.0
    assert ct.name == name
    assert ct.log_message.strip()


def test_codetimer_with_threshold_in_microseconds_not_logs_message(capsys):
    from linetimer import CodeTimer

    name = "name"

    ct = CodeTimer(name, unit='us', threshold=100000)

    with ct:
        sleep(0.01)

    assert ct.took < 100000.0
    assert ct.name == name
    assert not ct.log_message.strip()


def test_codetimer_with_threshold_in_nanoseconds_not_logs_message(capsys):
    from linetimer import CodeTimer

    name = "name"

    ct = CodeTimer(name, unit='ns', threshold=100000000)

    with ct:
        sleep(0.01)

    assert ct.took < 100000000.0
    assert ct.name == name
    assert not ct.log_message.strip()


log_message = None

def test_decorator():
    from linetimer import linetimer

    def save_message(msg):
        global log_message
        log_message = msg

    @linetimer(logger_func=save_message)
    def foo_dont_show_args(a, b='default'):
        pass

    foo_dont_show_args(1)
    assert log_message.startswith("Code block 'foo_dont_show_args' took")

    @linetimer(show_args=True, logger_func=save_message)
    def foo_show_args(a='default_a', b='default'):
        pass

    foo_show_args(1)
    assert log_message.startswith("Code block 'foo_show_args(1)' took")

    foo_show_args('a', 'b')
    assert log_message.startswith("Code block 'foo_show_args('a', 'b')' took")

    foo_show_args(1, b='b')
    assert log_message.startswith("Code block 'foo_show_args(1, b='b')' took")

    foo_show_args(b='b')
    assert log_message.startswith("Code block 'foo_show_args(b='b')' took")

    foo_show_args([None],{})
    assert log_message.startswith("Code block 'foo_show_args([None], {})' took")

    @linetimer(name='my name', logger_func=save_message)
    def foo_show_args(a, b='default'):
        pass

    foo_show_args(1)
    assert log_message.startswith("Code block 'my name' took")

    class FooClass:
        @linetimer(show_args=True, logger_func=save_message)
        def foo_show_args(self, a, b='default'):
            pass

        def __repr__(self):
            return '<FooClass>'

    fc = FooClass()
    fc.foo_show_args('a', 'b')
    assert log_message.startswith("Code block 'foo_show_args(<FooClass>, 'a', 'b')' took")






