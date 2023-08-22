'''
    This is the actual db tables required for this project, but never used in this project. It was never hosted or created.
    This uses sqlAlchemy(ORM) and shows the many many relationship between two tables.
'''

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class TrackingPlan(Base):
    id = Column(Integer, primary_key=True)
    display_name = Column(String(255), nullable=False)
    events = relationship('Event', secondary='tracking_plan_event', back_populates='tracking_plans')

class Event(Base):
    name = Column(String(255), nullable=False, primary_key=True)
    description = Column(String(255))
    rules = Column(JSONB, nullable=False)
    tracking_plans = relationship('TrackingPlan', secondary='tracking_plan_event', back_populates='events')

tracking_plan_event = Table('tracking_plan_event',
    Column('tracking_plan_id', Integer, ForeignKey('tracking_plan.id'), primary_key=True),
    Column('event_name', Integer, ForeignKey('event.name'), primary_key=True)
)
