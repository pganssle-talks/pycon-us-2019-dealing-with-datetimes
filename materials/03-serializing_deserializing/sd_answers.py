### Exercise: Write a function to store a message with metadata in JSON
import json
import logging

from dateutil import tz
from datetime import datetime, timezone

def encode_message(user_to: str, user_from: str, message: str) -> str:
    """Encode a message to be sent in JSON"""
    message_time = datetime.now(timezone.utc)

    to_encode = {
        "user_to": user_to,
        "user_from": user_from,
        "sent_epoch": message_time.timestamp(),
        "message": message
    }

    return json.dumps(to_encode)


### Exercise: Write a function to display the encoded message
def display_message(json_str: str) -> str:
    """Generate a display string for a JSON-encoded message"""
    decoded = json.loads(json_str)

    user_from = decoded["user_from"]
    sent_ts = decoded["sent_epoch"]
    message = decoded["message"]

    sent_dt = datetime.fromtimestamp(sent_ts)

    return (f"({sent_dt:%Y-%m-%d %H:%M:%S}) {user_from}\n" +
            f"{message}")


### Exercise: Write a function to parse log messages
def parse_log_line(line: str) -> dict:
    dt_str, level_str, name, message = line.split(' : ', 4)
    dt = datetime.fromisoformat(dt_str)

    return {
        'datetime': dt,
        'level': level_str,
        'name': name,
        'message': message,
    }


# Alternate version
def parse_log_line_enum(line: str) -> dict:
    """Alternative version: parse the log level as well

    If you wanted to support this in a generic parser, you may want an option
    to pass a custom mapping of level strings to levels.
    """

    dt_str, level_str, name, message = line.split(' : ', 4)
    dt = datetime.fromisoformat(dt_str)
    level = _parse_enum_level(level_str.strip())

    return {
        'datetime': dt,
        'level': level,
        'name': name,
        'message': message,
    }

_LOG_ENUM_MAP = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def _parse_enum_level(levelstr):
    if levelstr in _LOG_ENUM_MAP:
        return _LOG_ENUM_MAP[levelstr]

    if not levelstr.startswith("Level "):
        raise ValueError("Unknown logging level")
    else:
        return int(levelstr[len("Level "):])


### Bonus Exercise: Configure the logger to output timestamps in an ISO 8601 format
def get_iso_logger(name):
    # Get a logger
    logger = logging.getLogger(name)

    ch = logging.StreamHandler()
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)

    formatter = IsoFormatter("{asctime} : {levelname} : {name} : {message}",
                             style="{")
    ch.setFormatter(formatter)

    return logger


class IsoFormatter(logging.Formatter):
    def __init__(self, fmt=None, tzinfo=tz.tzlocal(), style="%"):
        super().__init__(fmt=fmt, datefmt=None, style=style)
        self._tzinfo = tzinfo

    def formatTime(self, record, *args, **kwargs):
        dt = datetime.fromtimestamp(record.created, tz=self._tzinfo)

        return dt.isoformat()




### Exercise: Configure JSON encoder/decoder to (de)serialize datetimes
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            tzi = obj.tzinfo
            if tzi is not None:
                if hasattr(tzi, 'name'):
                    tzi = tzi.name
                elif tzi is timezone.utc or tzi is tz.UTC:
                    tzi = "UTC"
                else:
                    raise ValueError("Time zone has no name to serialize")

            return {
                'datetime': obj.replace(tzinfo=None).isoformat(),
                'fold': obj.fold,
                'timezone': tzi
            }

        return super().default(obj)

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

def decode_datetime_hook(obj):
    if (isinstance(obj, dict) and len(obj) == 3 and
        all(x in obj for x in ('datetime', 'fold', 'timezone'))):
        # Decode a datetime from this
        dt = datetime.fromisoformat(obj['datetime'])
        fold = obj['fold']
        tzi = obj['timezone']
        if tzi is not None:
            tzi = get_annotated_tz(tzi)

        return dt.replace(fold=fold, tzinfo=tzi)
