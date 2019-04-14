from datetime import timedelta

def print_dt_tzinfo(dt, fmt_str='%Y-%m-%d %H:%M:%S%z'):
    s0 = f'{dt.strftime(fmt_str)}\n'
    s1 = f'    tzname: {dt.tzname():>5};'
    s1 += ' ' * max((1, 24 - len(s1)))

    utc_off = dt.utcoffset()
    if utc_off is not None:
        utc_off = utc_off / timedelta(hours=1)
        utc_off = f'{utc_off: >6.2f}h'
    else:
        utc_off = '     None'

    s2 = f'UTC Offset: {utc_off};'
    s2 += ' ' * max((1, 28 - len(s2)))

    dt_off = dt.dst()
    if dt_off is not None:
        dt_off = dt_off / timedelta(hours=1)
        dt_off = f'{dt_off:>8}h'
    else:
        dt_off = '     None'

    s2 += f'DST: {dt_off}'

    print(s0 + s1 + s2)
