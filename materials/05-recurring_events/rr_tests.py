import itertools as it
import rr_answers as rra

from datetime import datetime

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

