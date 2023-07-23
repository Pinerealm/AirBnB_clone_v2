#!/usr/bin/python3
""" State Module for HBNB project """
from .base_model import BaseModel, Base
from models import storage_type, storage
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class
    """
    if storage_type == 'db':
        __tablename__ = "states"
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
