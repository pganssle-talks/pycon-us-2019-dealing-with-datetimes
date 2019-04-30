import json
import logging
import sd_answers

from datetime import datetime, timedelta, timezone
from dateutil import tz

from freezegun import freeze_time

from helper_functions import TZEnvContext


### Exercise: Write a function to store a message with metadata in JSON
def test_encode_message_metadata(encode_message):
    user_to = "cool_beans1973"
    user_from = "xXx_the_matrix_xXx"
    message = "Test messageé"

    with freeze_time("2000-01-01T05:15:30.214333-05:00"):
        json_str = encode_message(user_to, user_from, message)

        print(f"Output:\n{json_str}")

        decoded = json.loads(json_str)
        assert decoded["user_to"] == user_to
        assert decoded["user_from"] == user_from
        assert decoded["sent_epoch"] == 946721730.214333
        assert decoded["message"] == message

    print("Passed!")


### Exercise: Write a function to retrieve and display the message
def test_display_message_metadata(display_message):
    user_to = "cool_beans1973"
    user_from = "xXx_the_matrix_xXx"
    message = "Test messageé"

    with freeze_time("2000-01-01T05:15:30.214333-05:00"):
        json_str = sd_answers.encode_message(user_to, user_from, message)

        with TZEnvContext('EST5EDT'):
            display_str = display_message(json_str)
        expected = f"(2000-01-01 05:15:30) {user_from}\n{message}"

        assert display_str == expected, \
            f"{display_str} != {expected}"

    print("Passed!")


### Exercise: Write a function to parse log messages
def test_parse_log_line(parse_log_line):
    offset = timezone(timedelta(hours=-4))
    lines = [
        ("2019-04-18T18:46:37.211352-04:00 : DEBUG :"
         " __main__iso : This is a message",
         {
             "datetime": datetime(2019, 4, 18, 18, 46, 37, 211352,
                                  tzinfo=offset),
             "level": "DEBUG",
             "name": "__main__iso",
             "message": "This is a message"
         }),
        ("2019-10-09T03:12:57.113347-04:00 : WARNING :"
         " __main__iso : This is a warning",
         {
             "datetime": datetime(2019, 10, 9, 3, 12, 57, 113347,
                                  tzinfo=offset),
             "level": "WARNING",
             "name": "__main__iso",
             "message": "This is a warning"
         }),
    ]

    warning_map = {
        'DEBUG': logging.DEBUG,
        'WARNING': logging.WARNING,
    }

    enum_mode = False
    for line, exp in lines:
        act = parse_log_line(line)

        # Allow implementations that map the level to an enum
        if not enum_mode and isinstance(act['level'], type(logging.DEBUG)):
            enum_mode = True

        if enum_mode:
            exp['level'] = warning_map[exp['level']]

        assert act == exp

    print("Passed!")


### Exercise: Write a JSON encoder and decoder hook for datetimes
def get_annotated_tz(name):
    """
    There is currently no supported way to get a string that can
    be passed to `gettz` from the `tzinfo` object itself, so until
    that is supported, hack this feature in.
    """
    tzi = tz.gettz(name)
    if tzi is not tz.UTC:
        tzi.name = name

    return tzi

NYC = get_annotated_tz("America/New_York")

dts = [
    datetime(2020, 1, 1, tzinfo=NYC),
    datetime(2020, 1, 1),
    datetime(2020, 1, 1, 14, 31, 11, 123456, tzinfo=get_annotated_tz('UTC')),
    datetime(2020, 1, 1, 14, tzinfo=timezone.utc),
    datetime(2020, 11, 1, 1, 30, fold=1, tzinfo=NYC)
]

def print_encodings(encoder):
    for dt in dts:
        print(encoder.encode(dt))

def test_round_trip(encoder, decoder):
    for dt in dts:
        dt_rt = decoder.decode(encoder.encode(dt))
        assert dt_rt == dt
        assert dt_rt.fold == dt.fold

    print("Passed!")
