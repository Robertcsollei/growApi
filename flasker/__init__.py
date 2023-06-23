from flasker.routes import relays
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from schema import session
from schema.logs import Log
from schema.utils import LogChangeType
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

startingLog = Log(None, change_type=LogChangeType.APP_START, changed_value=json.dumps(f"app: {__name__}"))
session.add(startingLog)
session.commit()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)


app.register_blueprint(relays.api)
