from flasker.routes import relays
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt

from schema import session
from schema.logs import Log
from schema.utils import LogChangeType
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
topic = '/flask/mqtt'

mqtt_client = Mqtt(app)

startingLog = Log(None, change_type=LogChangeType.APP_START, changed_value=json.dumps(f"app: {__name__}"))
session.add(startingLog)
session.commit()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)


app.register_blueprint(relays.api)
