import os
import textwrap
import time

from itertools import groupby, zip_longest
from datetime import datetime, timedelta


def print_dtlist(dtlist):
    values = False
    for dt in dtlist:
        print(dt)
        values = True

    if not values:
        print("Empty")


def print_dts(dts_list):
    format_str = '|'.join(['{:^40}'] * 2)
    print(format_str.format('start_date', '+relativedelta'))
    print(format_str.format(*(['-' * 40] * 2)))
    for dts in dts_list:
        dts_map = map(lambda d: d.strftime('%Y-%m-%d'), dts)
        print(format_str.format(*dts_map))


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


def _get_schedule_grid(schedule):
    gby = groupby(schedule,
                  key=datetime.date)

    l = [(g, [val.time() for val in vals])
         for g, vals in gby]

    labels, vals = zip(*l)

    # Load the top label (date) and the bottom label (day of week), e.g.:
    #
    #  2016-11-07  |  2016-11-08 |  ...
    #     Mon      |      Tue    |  ...
    date_labels = [dt.strftime('%Y-%m-%d') for dt in labels]
    day_labels = [dt.strftime('%a') for dt in labels]


    # Convert the columns (days) into rows in the table
    rows = []
    for val_row in zip_longest(*vals, fillvalue=None):
        row = []

        for val in val_row:
            if val is None:
                row.append('')
            else:
                row.append(val.strftime("%H:%M"))

        rows.append(row)

    return rows, date_labels, day_labels

def _render_schedule_html(rows, date_labels, day_labels, style=None):
    style = style or _get_default_style()

    # Convert the row lists into HTML
    def make_table_row(row, cls_attr):
        rowstr = ""
        for cell in row:
            rowstr += f"    <td>{cell}</td>\n"

        class_str = f'class="{cls_attr}"' if cls_attr else ''

        return f"<tr {class_str}>\n{rowstr}</tr>"

    table_row_strs = ""
    table_row_strs += make_table_row(date_labels, "header datehead")
    table_row_strs += make_table_row(day_labels, "header wdayhead")

    for ii, row in enumerate(rows):
        oddstr = "odd_row" if ii % 2 else "even_row"
        table_row_strs += make_table_row(row, f"rows {oddstr}")

    table_row_strs = textwrap.indent(table_row_strs, " " * 4)

    return f"{style}<table>\n{table_row_strs}\n</table>"

def _get_default_style():
    return textwrap.dedent("""
    <style type="type/css">

    .header tr {
        font-size: 18px;
        background #cacaca;
    }

    .rows tr {
        font-size: 16px;
    }

    .odd_row {
        background-color: rgb(245, 245, 245);
    }

    .even_row {
        background-color: rgb(255, 255, 255);
    }
    </style>
    """).strip()


def display_bus_schedule(schedule, style=None):
    from IPython.display import display, HTML

    schedule_grid, *labels = _get_schedule_grid(schedule)
    html = _render_schedule_html(schedule_grid, *labels, style=style)

    display(HTML(html))


class TZContextBase:
    """
    Base class for a context manager which allows changing of time zones.

    Subclasses may define a guard variable to either block or or allow time
    zone changes by redefining ``_guard_var_name`` and ``_guard_allows_change``
    The default is that the guard variable must be affirmatively set.

    Subclasses must define ``get_current_tz`` and ``set_current_tz``.
    """
    _guard_var_name = "DATEUTIL_MAY_CHANGE_TZ"
    _guard_allows_change = True

    def __init__(self, tzval):
        self.tzval = tzval
        self._old_tz = None

    @classmethod
    def tz_change_allowed(cls):
        """
        Class method used to query whether or not this class allows time zone
        changes.
        """
        guard = bool(os.environ.get(cls._guard_var_name, False))

        # _guard_allows_change gives the "default" behavior - if True, the
        # guard is overcoming a block. If false, the guard is causing a block.
        # Whether tz_change is allowed is therefore the XNOR of the two.
        return guard == cls._guard_allows_change

    @classmethod
    def tz_change_disallowed_message(cls):
        """ Generate instructions on how to allow tz changes """
        msg = ('Changing time zone not allowed. Set {envar} to {gval} '
               'if you would like to allow this behavior')

        return msg.format(envar=cls._guard_var_name,
                          gval=cls._guard_allows_change)

    def __enter__(self):
        if not self.tz_change_allowed():
            raise ValueError(self.tz_change_disallowed_message())

        self._old_tz = self.get_current_tz()
        self.set_current_tz(self.tzval)

    def __exit__(self, type, value, traceback):
        if self._old_tz is not None:
            self.set_current_tz(self._old_tz)

        self._old_tz = None

    def get_current_tz(self):
        raise NotImplementedError

    def set_current_tz(self):
        raise NotImplementedError


class TZEnvContext(TZContextBase):
    """
    Context manager that temporarily sets the `TZ` variable (for use on
    *nix-like systems). Because the effect is local to the shell anyway, this
    will apply *unless* a guard is set.

    If you do not want the TZ environment variable set, you may set the
    ``DATEUTIL_MAY_NOT_CHANGE_TZ_VAR`` variable to a truthy value.
    """
    _guard_var_name = "DATEUTIL_MAY_NOT_CHANGE_TZ_VAR"
    _guard_allows_change = False

    def get_current_tz(self):
        return os.environ.get('TZ', UnsetTz)

    def set_current_tz(self, tzval):
        if tzval is UnsetTz and 'TZ' in os.environ:
            del os.environ['TZ']
        else:
            os.environ['TZ'] = tzval

        time.tzset()

UnsetTz = object()
