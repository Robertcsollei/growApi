
from flask import Blueprint, request
from schema.relay import Relay
from schema.logs import Log
from schema.utils import serialize_relay_update_log, LogChangeType
from schema import session
import json

api = Blueprint("api", __name__)


@api.route("/relays", methods=["GET", "PUT", "POST"])
def relays():
    if request.method == "GET":
        # Show all the relays
        return getAllRelaysAsJson()
    elif request.method == "POST":
        # Create or update multiple relays
        data = request.get_json()

        if not isinstance(data, list):
            res = "Invalid payload format. Expected an array of relays.", 400
            log = Log(None, change_type=LogChangeType.ERROR,
                      changed_value=json.dumps(res))
            session.add(log)
            session.commit()
            return res

        for relay_data in data:
            relay_id = relay_data.get("uuid")
            relay = session.query(Relay).filter_by(uuid=relay_id).first()

            if not relay:
                # Create a new relay
                create_relay(data=data)
            else:
                # Update an existing relay
                update_relay(relay=relay, data=data)

        session.commit()
        return getAllRelaysAsJson(), 201


@api.route("/relay/<relay_id>", methods=["GET", "PUT", "POST"])
def relay(relay_id):
    if request.method == "GET":
        relay = session.query(Relay).filter_by(uuid=relay_id).first()
        if not relay:
            res = f"Relay '{relay_id}' not found", 404
            log = Log(None, change_type=LogChangeType.ERROR,
                      changed_value=json.dumps(res))
            session.add(log)
            session.commit()
            return res
        return relay.to_dict()

    elif request.method == "PUT":

        # Update an existing relay
        relay = session.query(Relay).filter_by(uuid=relay_id).first()
        if not relay:
            res = "Relay not found", 404
            log = Log(None, change_type=LogChangeType.ERROR,
                      changed_value=json.dumps(res))
            session.add(log)
            session.commit()
            return "Relay not found", 404
        data = request.get_json()
        result = update_relay(relay=relay, data=data)
        session.commit()
        return result

    elif request.method == "POST":

        data = request.get_json()
        result = create_relay(data=data)
        session.commit()
        return result


def getAllRelaysAsJson():
    allRelays = session.query(Relay).all()
    response = [relay.to_dict() for relay in allRelays]
    return json.dumps(response)

def update_relay(relay, data):

    json_data = serialize_relay_update_log(relay=relay, relay_data=data)
    if data.get("label"):
        relay.label = data.get("label", relay.label)
    if data.get("state"):
        relay.state = data.get("state", relay.state)
    log = Log(target=relay.uuid, change_type=LogChangeType.UPDATED,
              changed_value=json_data)
    session.add(log)
    print("should update log")
    session.commit()
    return relay.to_dict(), 202

def create_relay(data):
    newRelay = Relay(label=data.get("label"), state=data.get("state"))
    log = Log(target=relay.uuid, change_type=LogChangeType.CREATED)
    session.add(newRelay)
    session.add(log)
    return newRelay.to_dict(), 201