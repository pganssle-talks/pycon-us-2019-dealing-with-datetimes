from dateutil.utils import today
from datetime import timedelta, tzinfo

from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

### Exercise: Try out a few absolute deltas
def march_3rd_this_year():
    """Get March 3rd of this year"""
    return today() + relativedelta(month=3, day=3)

def today_in_1951():
    """Get the current date in 1951 (no error on February 29th)"""
    return today() + relativedelta(year=1951)

def today_at_1215():
    """Get a datetime representing 12:15 today"""
    return today() + relativedelta(hour=12, minute=15)


### Bonus Exercise:
def end_of_month(dt):
    return dt + relativedelta(months=1, day=1, days=-1)



### Exercise: Implement a tzinfo with the current US DST rules
class Eastern(tzinfo):
    def __init__(self):
        self._tznames = ("EST", "EDT")
        self._offsets = (timedelta(hours=-5), timedelta(hours=-4))
        self._dsts = (timedelta(hours=0), timedelta(hours=1))

        self._DST_START = relativedelta(month=3, day=1, weekday=SU(+2),
                                        hour=2, minute=0, second=0, microsecond=0)
        self._DST_END = relativedelta(month=11, day=1, weekday=SU(+1),
                                      hour=2, minute=0, second=0, microsecond=0)

        super().__init__()

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def tzname(self, dt):
        return self._tznames[self.is_dst(dt)]

    def utcoffset(self, dt):
        return self._offsets[self.is_dst(dt)]

    def dst(self, dt):
        return self._dsts[self.is_dst(dt)]

    def is_dst(self, dt):
        dst_start = dt + self._DST_START
        dst_end = dt + self._DST_END

        if dt.fold and (dst_end - timedelta(hours=5)) < dt < dst_end:
            return 0

        return int(dst_start <= dt < dst_end)

