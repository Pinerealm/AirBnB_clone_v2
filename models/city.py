#!/usr/bin/python3
"""The city module
"""
from .base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Defines the City class, inherits from BaseModel and Base (SQLAlchemy)

    Attributes:
        name (str): The city name
        state_id (str): The state id
        places (list): The list of Place objects linked to the city (db only)
    """
    if storage_type == 'db':
        __tablename__ = "cities"
        __table_args__ = {'mysql_default_charset': 'latin1'}
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", backref="cities", cascade="all, delete")

    else:
        name = ""
        state_id = ""
