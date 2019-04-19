### Exercise: Write a function to store a message with metadata in JSON
import json

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
