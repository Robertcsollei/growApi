import json
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LogChangeType(Enum):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'
    APP_START = "app_start"
    INITIALIZED_NEW_DATABASE = "initialized_new_database"
    ERROR = 'error'


def serialize_relay_update_log(relay, relay_data):
    logData = {}
    logData['old_label'] = relay_data.get("label")
    logData['old_state'] = relay_data.get("state")
    logData['new_label'] = relay.label
    logData['new_state'] = relay.state
    json_data = json.dumps(logData)
    return json_data



