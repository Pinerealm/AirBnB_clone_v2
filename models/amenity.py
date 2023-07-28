#!/usr/bin/python3
"""The amenity module
"""
from .base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Defines the Amenity class, inherits from BaseModel

    Attributes:
        name (str): The name of the amenity
        place_amenities (list): Represents the Place-Amenity relationship
    """
    if storage_type == 'db':
        __tablename__ = "amenities"
        __table_args__ = {'mysql_default_charset': 'latin1'}
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity",
                                       back_populates="amenities")

    else:
        name = ""
