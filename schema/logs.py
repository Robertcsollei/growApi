from datetime import datetime
from sqlalchemy import Column, JSON, Enum, Integer,  DateTime, ForeignKey
from sqlalchemy.orm import relationship
from schema.utils import LogChangeType, Base



class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    target = Column(Integer, ForeignKey('relays.uuid'), nullable=True)
    change_type = Column(Enum(LogChangeType))
    changed_value = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    relay = relationship("Relay")

    def __init__(self, target, change_type, changed_value = None):
        self.target = target
        self.change_type = change_type
        self.changed_value = changed_value


