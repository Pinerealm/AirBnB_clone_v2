#!/usr/bin/python3
""" State Module for HBNB project """
from .base_model import BaseModel, Base
from models import storage_type, storage
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """The Amenity class
    """
    if storage_type == 'db':
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity",
                                       back_populates="amenities")
        
    else:
        name = ""
