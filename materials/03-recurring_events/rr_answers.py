from dateutil.rrule import rrule, rruleset
from dateutil.rrule import YEARLY, MONTHLY, WEEKLY, DAILY
from dateutil.rrule import HOURLY, MINUTELY, SECONDLY
from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU
from datetime import datetime

from itertools import zip_longest

### Exercise: Martin Luther King Day

MLK_DAY = rrule(
    dtstart=datetime(1986, 1, 20),      # First celebration
    freq=YEARLY,                        # Occurs once per year
    bymonth=1,                          # In January
    byweekday=MO(+3),                   # On the 3rd Monday
)


### Exercise: Build a bus schedule
dtstart = datetime(2020, 10, 1)
WEEKDAYS = (MO, TU, WE, TH, FR)
WEEKENDS = (SA, SU)

def get_weekday_schedule():
    # Every hour on the 37 between 6:37 and 22:37
    weekday_schedule = rrule(freq=DAILY,
                             byhour=range(6, 23),
                             byminute=37,
                             byweekday=WEEKDAYS,
                             dtstart=dtstart)

    return weekday_schedule


def get_weekend_schedule():
    # Every hour on the 7 from 08:07 to 19:07
    weekend_schedule = rrule(freq=DAILY,
                             byhour=range(8, 20),
                             byminute=7,
                             byweekday=WEEKENDS,
                             dtstart=dtstart)

    return weekend_schedule


def get_base_schedule():
    bus_schedule = rruleset()
    bus_schedule.rrule(get_weekday_schedule())
    bus_schedule.rrule(get_weekend_schedule())

    return bus_schedule


def test_basic_bus_schedule_expl():
    """
    Extra test for these, since the workbook tests are defined in terms
    of these answers
    """
    exp = [datetime(2020, 10, 9, 6, 37).replace(hour=h)
           for h in [ 6,  7,  8,  9, 10, 11, 12, 13, 14,
                     15, 16, 17, 18, 19, 20, 21, 22]]

    exp += [datetime(2020, 10, 10, 8, 7).replace(hour=h)
            for h in [ 8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]

    exp += [datetime(2020, 10, 11, 8, 7).replace(hour=h)
            for h in [ 8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]

    exp += [datetime(2020, 10, 12, 6, 37).replace(hour=h)
            for h in [ 6,  7,  8,  9, 10, 11, 12, 13, 14,
                      15, 16, 17, 18, 19, 20, 21, 22]]

    act = get_base_schedule().between(datetime(2020, 10, 9),
                                      datetime(2020, 10, 13))

    for dt_act, dt_exp in zip_longest(act, exp):
        assert dt_act == dt_exp

test_basic_bus_schedule_expl()


### Exercise: Reduced evening bus service
def get_evening_schedule():
    bus_schedule = get_base_schedule()
    weekday_schedule = get_weekday_schedule()

    # Get the 19:37 and 21:37 entries to exclude from the rule
    weekday_evenings = weekday_schedule.replace(byhour=(19, 21))

    bus_schedule.exrule(weekday_evenings)

    return bus_schedule


def test_evening_bus_schedule():
    exp = [datetime(2020, 10, 9, 6, 37).replace(hour=h)
           for h in [ 6,  7,  8,  9, 10, 11, 12, 13, 14,
                     15, 16, 17, 18, 20, 22]]

    act = get_evening_schedule().between(datetime(2020, 10, 9),
                                         datetime(2020, 10, 10))

    for dt_act, dt_exp in zip_longest(act, exp):
        assert dt_act == dt_exp

test_evening_bus_schedule()


### Exercise: Bus service cancelled on election day
def get_no_election_schedule():
    # Start with the previous schedule
    bus_schedule = get_evening_schedule()

    # Iterate over all the recurrences on November 3rd, 2020 and exclude them
    for dt in bus_schedule.between(datetime(2020, 11, 3),
                                   datetime(2020, 11, 4)):
        bus_schedule.exdate(dt)

    return bus_schedule


def test_get_no_election_schedule():
    exp = [
        datetime(2020, 11, 2, 17, 37),
        datetime(2020, 11, 2, 18, 37),
        datetime(2020, 11, 2, 20, 37),
        datetime(2020, 11, 2, 22, 37),
        datetime(2020, 11, 4,  6, 37),
        datetime(2020, 11, 4,  7, 37),
    ]

    act = get_no_election_schedule().between(datetime(2020, 11, 2, 17),
                                             datetime(2020, 11, 4, 8))

    for dt_act, dt_exp in zip_longest(act, exp):
        assert dt_act == dt_exp

test_get_no_election_schedule()


### Exercise: Limited service restoration

def get_final_schedule():
    # Start with previous schedule
    bus_schedule = get_no_election_schedule()

    # Add our two rdates
    bus_schedule.rdate(datetime(2020, 11, 3, 4, 32))
    bus_schedule.rdate(datetime(2020, 11, 3, 19, 39))

    return bus_schedule


def test_final_schedule():
    exp = [
        datetime(2020, 11, 2, 17, 37),
        datetime(2020, 11, 2, 18, 37),
        datetime(2020, 11, 2, 20, 37),
        datetime(2020, 11, 2, 22, 37),
        datetime(2020, 11, 3,  4, 32),
        datetime(2020, 11, 3, 19, 39),
        datetime(2020, 11, 4,  6, 37),
        datetime(2020, 11, 4,  7, 37),
    ]

    act = get_final_schedule().between(datetime(2020, 11, 2, 17),
                                      datetime(2020, 11, 4, 8))

    for dt_act, dt_exp in zip_longest(act, exp):
        assert dt_act == dt_exp

test_final_schedule()

