from dateutil import rrule
from datetime import datetime

### Exercise: Martin Luther King Day

MLK_DAY = rrule.rrule(
    dtstart=datetime(1986, 1, 20),      # First celebration
    freq=rrule.YEARLY,                  # Occurs once per year
    bymonth=1,                          # In January
    byweekday=rrule.MO(+3),             # On the 3rd Monday
)
