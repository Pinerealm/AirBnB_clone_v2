#!/usr/bin/python3
"""The state module
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import storage_type

from .base_model import Base, BaseModel


class State(BaseModel, Base):
    """Defines the State class, inherits from BaseModel

    Attributes:
        name (str): The state name
    """
    if storage_type == 'db':
        __tablename__ = "states"
        __table_args__ = {'mysql_default_charset': 'latin1'}
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")

    else:
        name = ""

        @property
        def cities(self):
            """Gets the list of cities associated with the current state.
            """
            from .city import City
            city_list = []
            for value in storage.all(City).values():
                if value.state_id == self.id:
                    city_list.append(value)
            return city_list
