from datetime import datetime, timedelta, timezone
from functools import total_ordering
UTC = timezone.utc

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
@total_ordering
class AbsoluteDateTime(datetime):
    """A version of datetime that uses only elapsed time semantics"""
    def __add__(self, other):
        # __add__ is only supported between datetime and timedelta
        dt = datetime.__add__(self.astimezone(UTC), other)
        dt = dt.astimezone(self.tzinfo)

        # Required to support the case where tzinfo is None
        dt = dt.replace(tzinfo=self.tzinfo)
        return self.__class__.as_absolute_datetime(dt)

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

    @classmethod
    def as_absolute_datetime(cls, dt):
        """Construct an AbsoluteDatetime from any datetime subclass"""
        return cls(*dt.timetuple()[0:6], microsecond=dt.microsecond,
                   tzinfo=dt.tzinfo, fold=dt.fold)

@total_ordering
class WallDateTime(datetime):
    """A version of datetime that uses only wall time semantics"""
    def __add__(self, other):
        # __add__ is only supported between datetime and timedelta
        dt = datetime.__add__(self.replace(tzinfo=None), other)

        # Required to support the case where tzinfo is None
        dt = dt.replace(tzinfo=self.tzinfo)
        return self.__class__.as_wall_datetime(dt)

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

    @classmethod
    def as_wall_datetime(cls, dt):
        """Construct a WallDateTime from any datetime subclass"""
        return cls(*dt.timetuple()[0:6], microsecond=dt.microsecond,
                   tzinfo=dt.tzinfo, fold=dt.fold)

