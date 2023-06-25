#!/usr/bin/python3
""" Review module for the HBNB project """
from .base_model import BaseModel
from models import storage_type
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """The review class
    """
    if storage_type == 'db':
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    else:
        place_id = ""
        user_id = ""
        text = ""
