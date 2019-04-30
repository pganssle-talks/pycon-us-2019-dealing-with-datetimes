from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

from dateutil import tz

import tz_answers
from tz_answers import AmbiguousTimeError, NonExistentTimeError

### Exercise: Implement a UTC class
def test_utc(utc):
    test_cases = [
        datetime(1, 1, 1),
        datetime(1857, 2, 7),
        datetime(1970, 1, 1),
        datetime(2010, 3, 21, 2, 16)
    ]

    for dt in test_cases:
        dt_act = dt.replace(tzinfo=utc)
        dt_exp = dt.replace(tzinfo=timezone.utc)

        assert dt_act.tzname() == dt_exp.tzname(), \
            f'tznames must match for {dt}'
        assert dt_act.utcoffset() == dt_exp.utcoffset(), \
            f'utcoffset must match for {dt}'

        dst = dt_act.dst()
        if dst == timedelta(0):
            print("Warning: Standard library returns None")
        else:
            assert dst is None, f'dst must match for {dt}: {dst} != {None}'

    print("Passed!")


### Exercise: Build a pytz-style exception-based localizer with dateutil
@contextmanager
def assert_raises(err_type):
    try:
        yield
    except err_type:
        pass
    else:
        raise AssertionError(f"Failed to raise {err_type} exception")

def assert_dt_equal(dt1, dt2):
    """
    datetime equality is a bit more complicated than it may seem when dealing
    with ambiguous and imaginary datetimes
    """

    fail_msg = f"{dt1} != {dt2}"
    assert dt1.astimezone(tz.UTC) == dt2.astimezone(tz.UTC), fail_msg
    assert dt1.tzname() == dt2.tzname(), fail_msg
    assert dt1.utcoffset() == dt2.utcoffset(), fail_msg
    assert dt1.dst() == dt2.dst(), fail_msg

def test_localize(localize):
    NYC = tz.gettz('America/New_York')
    with assert_raises(AmbiguousTimeError):
        localize(datetime(2004, 10, 31, 1, 30), NYC, is_dst=None)

    with assert_raises(NonExistentTimeError):
        localize(datetime(2004, 4, 4, 2, 30), NYC, is_dst=None)

    with assert_raises(ValueError):
        localize(datetime(2004, 10, 31, 1, 30, tzinfo=NYC), NYC)

    assert_dt_equal(
        localize(datetime(2004, 10, 31, 1, 30), NYC, is_dst=False),
        datetime(2004, 10, 31, 1, 30, fold=1, tzinfo=NYC))

    assert_dt_equal(
        localize(datetime(2004, 10, 31, 1, 30), NYC, is_dst=True),
        datetime(2004, 10, 31, 1, 30, fold=0, tzinfo=NYC))

    print("Passed!")


### Exercise: Implement explicit wall-time and absolute-time arithmetic
NYC = tz.gettz('America/New_York')
SUB_PAIRS = [
    (datetime(2018, 3, 11, 1, tzinfo=tz.gettz('America/Los_Angeles')),
     datetime(2018, 3, 11, 1, tzinfo=NYC)),
    (datetime(2018, 3, 11, 8, 30, tzinfo=NYC),
     datetime(2018, 3, 10, 13, 30, tzinfo=NYC)),
]

def test_wall_sub(wall_sub):
    for dt1, dt2 in SUB_PAIRS:
        assert wall_sub(dt1, dt2) == tz_answers.wall_sub(dt1, dt2), \
            f"wall_sub({dt1}, {dt2})"

    print("Passed!")


def test_absolute_sub(absolute_sub):
    for dt1, dt2 in SUB_PAIRS:
        assert absolute_sub(dt1, dt2) == tz_answers.absolute_sub(dt1, dt2), \
            f"absolute_sub({dt1}, {dt2})"

    print("Passed!")


ADD_PAIRS = [
    (datetime(2018, 3, 10, 13, tzinfo=NYC), timedelta(days=1)),
]

def test_wall_add(wall_add):
    for dt, off in ADD_PAIRS:
        assert wall_add(dt, off) == tz_answers.wall_add(dt, off), \
            f"wall_sub({dt}, {off})"

    print("Passed!")


def test_absolute_add(absolute_add):
    for dt, off in ADD_PAIRS:
        assert absolute_add(dt, off) == tz_answers.absolute_add(dt, off), \
            f"absolute_add({dt}, {off})"

    print("Passed!")
