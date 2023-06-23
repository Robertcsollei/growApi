
from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema.relay import Relay
from schema.logs import Log
from schema.utils import Base, LogChangeType


DATABASE_PATH = 'sqlite:///data/database.db'
populateDatabase = not database_exists(DATABASE_PATH)

engine = create_engine(DATABASE_PATH, echo=True, connect_args={
                       'check_same_thread': False})
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


if populateDatabase:
    print("Recreating Database...")

    r1 = Relay(False, "Pump")
    r2 = Relay(False, "Right - A")
    r3 = Relay(False, "Right - B")
    r4 = Relay(False, "Left - A")
    r5 = Relay(False, "Left - B")
    log1 = Log(None, LogChangeType.INITIALIZED_NEW_DATABASE)

    session.add(r1)
    session.add(r2)
    session.add(r3)
    session.add(r4)
    session.add(r5)
    session.add(log1)

    session.commit()
