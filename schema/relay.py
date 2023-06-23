from sqlalchemy import Column, String, Integer, Boolean
from schema.utils import Base

class Relay(Base):

    __tablename__ = "relays"

    uuid = Column("uuid", Integer, primary_key=True, autoincrement=True)
    state = Column("state", Boolean)
    label = Column("label", String)

    def __init__(self, state: bool, label: str):
        self.state = state
        self.label = label

    def __repr__(self):
        return f"uuid: {self.uuid} -- Relay '{self.label}' is on: {self.state}"

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "state": self.state,
            "label": self.label
        }
