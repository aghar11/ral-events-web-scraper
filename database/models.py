'''
 models.py
 
 This file contains the basic data model for an Event
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, create_engine
from database.config import DATABASE_URL

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        UniqueConstraint("name", "startDate", "location", name="uq_event_identity"),
    )

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    url = Column(String, nullable=False)

# Create engine and table
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)