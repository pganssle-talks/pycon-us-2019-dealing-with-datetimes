from datetime import datetime, timedelta, timezone, tzinfo
from functools import total_ordering

from dateutil import tz

UTC = timezone.utc


### Exercise: Implement a UTC class
class UTC_(tzinfo):
    def tzname(self, dt):
        return "UTC"

    def utcoffset(self, dt):
        return timedelta(0)

    def dst(self, dt):
        return None


### Exercise: Current time in multiple time zones
def now_in_zones(tz_list):
    # For now I'll fib and pretend the current datetime is 2020
    dt_utc = datetime(2020, 1, 1, tzinfo=tz.gettz('America/New_York'))
    for tzstr in tz_list:
        dt = dt_utc.astimezone(tz.gettz(tzstr))
        print(f"{tzstr + ':':<25} {dt}")


### Exercise: Build a pytz-style exception-based localizer with dateutil
class AmbiguousTimeError(Exception):
    """Raised if an ambiguous time is detected"""

class NonExistentTimeError(Exception):
    """Raised if an imaginary time is detected"""


def localize(dt, tzi, is_dst=False):
    """
    Mimicks `pytz`'s `localize` function using the `fold` attribute.
    """
    if dt.tzinfo is not None:
        raise ValueError('localize can only be used with naive datetimes')

    if is_dst is None:
        # If is_dst is None, we want to raise an error for uncertain situations
        dt_out = dt.replace(tzinfo=tzi)
        if tz.datetime_ambiguous(dt_out):
            raise AmbiguousTimeError(f"Ambiguous time {dt} in zone {tzi}")
        elif not tz.datetime_exists(dt_out):
            raise NonExistentTimeError(f"Time {dt} does not exist in zone {tzi}")
    else:
        dt_out = dt.replace(fold=(not is_dst), tzinfo=tzi)

    return dt_out


### Exercise: Implement explicit wall-time and absolute-time arithmetic
def wall_add(dt: datetime, offset: timedelta) -> datetime:
    """Addition with "wall-time" semantics"""
    return dt + offset

def wall_sub(dt: datetime, other: datetime) -> timedelta:
    """Subtraction with "wall time" semantics"""
    if isinstance(other, timedelta):
        return wall_add(dt, -1 * other)

    return dt.replace(tzinfo=None)- other.replace(tzinfo=None)

def absolute_add(dt: datetime, offset: timedelta) -> datetime:
    """Addition with "absolute time" semantics"""
    return (dt.astimezone(UTC) + offset).astimezone(dt.tzinfo)

def absolute_sub(dt: datetime, other: datetime) -> timedelta:
    if isinstance(other, timedelta):
        return absolute_add(dt, -1 * other)

    return (dt.astimezone(UTC) - other.astimezone(UTC))

### Exercise (bonus): Implement a `AbsoluteDateTime` and `WallDateTime`
class ExplicitSemanticsDatetime(datetime):
    def as_datetime(self):
            return datetime(self.year, self.month, self.day,
                            self.hour, self.minute, self.second,
                            self.microsecond, fold=self.fold,
                            tzinfo=self.tzinfo)

    @classmethod
    def from_datetime(cls, dt):
        """Construct an AbsoluteDatetime from any datetime subclass"""
        return cls(*dt.timetuple()[0:6], microsecond=dt.microsecond,
                   tzinfo=dt.tzinfo, fold=dt.fold)


@total_ordering
class AbsoluteDateTime(ExplicitSemanticsDatetime):
    """A version of datetime that uses only elapsed time semantics"""
    def __add__(self, other):
        # __add__ is only supported between datetime and timedelta
        dt = datetime.__add__(self.astimezone(UTC), other)
        dt = dt.astimezone(self.tzinfo)

        # Required to support the case where tzinfo is None
        dt = dt.replace(tzinfo=self.tzinfo)
        return self.__class__.from_datetime(dt)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            # Use __add__ implementation if it's datetime and timedelta
            return self + (-1) * other
        else:
            return datetime.__sub__(self.astimezone(UTC),
                                    other.astimezone(UTC))

    def __eq__(self, other):
        return datetime.__eq__(self.astimezone(UTC), other.astimezone(UTC))

    def __lt__(self, other):
        return datetime.__lt__(self.astimezone(UTC), other.astimezone(UTC))

    def astimezone(self, tz):
            return datetime.astimezone(self.as_datetime(), tz)


@total_ordering
class WallDateTime(ExplicitSemanticsDatetime):
    """A version of datetime that uses only wall time semantics"""
    def __add__(self, other):
        # __add__ is only supported between datetime and timedelta
        dt = datetime.__add__(self.replace(tzinfo=None), other)

        # Required to support the case where tzinfo is None
        dt = dt.replace(tzinfo=self.tzinfo)
        return self.__class__.from_datetime(dt)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            # Use __add__ implementation if it's datetime and timedelta
            return self + (-1) * other
        else:
            return datetime.__sub__(self.replace(tzinfo=None),
                                    other.replace(tzinfo=None))

    def __eq__(self, other):
        return datetime.__eq__(self.replace(tzinfo=None),
                               other.replace(tzinfo=None))

    def __lt__(self, other):
        return datetime.__lt__(self.replace(tzinfo=None),
                               other.replace(tzinfo=None))
