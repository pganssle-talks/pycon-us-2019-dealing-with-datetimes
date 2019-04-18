### Exercise: Write a function to store a message with metadata in JSON
import json
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

