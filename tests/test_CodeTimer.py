from time import sleep


def test_single_blank():
    from linetimer import CodeTimer

    ct = CodeTimer()

    with ct:
        sleep(1)

    assert ct.took >= 1000.0


def test_single_named():
    from linetimer import CodeTimer

    name = "name"

    ct = CodeTimer(name)

    with ct:
        sleep(1)

    assert ct.took >= 1000.0
    assert ct.name == name


def test_two_named():
    from linetimer import CodeTimer

    name1 = "name1"
    name2 = "name2"

    ct1 = CodeTimer(name1)

    with ct1:
        sleep(1)

    ct2 = CodeTimer(name2)

    with ct2:
        sleep(2)

    assert ct1.took >= 1000.0
    assert ct1.name == name1

    assert ct2.took >= 2000.0
    assert ct2.name == name2


def test_two_nested():
    from linetimer import CodeTimer

    name1 = "outer"
    name2 = "inner"

    ct1 = CodeTimer(name1)

    with ct1:
        sleep(1)

        ct2 = CodeTimer(name2)

        with ct2:
            sleep(2)

    assert ct1.took >= 3000.0
    assert ct1.name == name1

    assert ct2.took >= 2000.0
    assert ct2.name == name2


def test_time_unit():
    from linetimer import CodeTimer

    unit1 = 's'

    ct1 = CodeTimer('ct_' + unit1, unit=unit1)

    with ct1:
        sleep(1)

    assert ct1.took >= 1
    assert ct1.unit == unit1

    unit2 = 'xyz'

    ct2 = CodeTimer('ct_' + unit2, unit=unit2)

    with ct2:
        sleep(1)

    assert ct2.took >= 1000
    assert ct2.unit == unit2
