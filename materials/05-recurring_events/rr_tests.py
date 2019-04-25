import itertools as it
import rr_answers as rra

from datetime import datetime

### Exercise: Martin Luther King Day
def test_mlk_day(mlk_day):
    test_cases = [
        ((datetime(1970, 1, 1), datetime(1980, 1, 1)),
         []),
        ((datetime(1980, 1, 1), datetime(1989, 1, 1)),
         [datetime(1986, 1, 20),
          datetime(1987, 1, 19),
          datetime(1988, 1, 18)]),
        ((datetime(2017, 2, 1), datetime(2022, 2, 1)),
         [datetime(2018, 1, 15, 0, 0),
          datetime(2019, 1, 21, 0, 0),
          datetime(2020, 1, 20, 0, 0),
          datetime(2021, 1, 18, 0, 0),
          datetime(2022, 1, 17, 0, 0)]
         ),
    ]

    for (between_args, expected) in test_cases:
        assert mlk_day.between(*between_args) == expected

    print("Passed!")


######
## Tests for bus schedule exercises
def _test_bus_schedule(bus_schedule, exp_sched):
    dt_limits = (datetime(2020, 9, 1),
                 datetime(2021, 1, 31))

    act = bus_schedule.between(*dt_limits)
    exp = bus_schedule.between(*dt_limits)

    for dt_act, dt_exp in it.zip_longest(act, exp):
        assert dt_act == dt_exp

    print("Passed!")

def test_basic_bus_schedule(bus_schedule):
    exp_sched = rra.get_base_schedule()

    _test_bus_schedule(bus_schedule, exp_sched)

def test_evening_bus_schedule(bus_schedule):
    exp_sched = rra.get_evening_schedule()

    _test_bus_schedule(bus_schedule, exp_sched)


def test_no_election_day(bus_schedule):
    exp_sched = rra.get_no_election_schedule()

    _test_bus_schedule(bus_schedule, exp_sched)

def test_final_schedule(bus_schedule):
    exp_sched = rra.get_final_schedule()

    _test_bus_schedule(bus_schedule, exp_sched)

