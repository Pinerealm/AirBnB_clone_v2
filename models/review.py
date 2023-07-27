#!/usr/bin/python3
"""The review module
"""
from .base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Defines the Review class, inherits from BaseModel and Base (SQLAlchemy)

    Attributes:
        place_id (str): The place id
        user_id (str): The user id
        text (str): The review text
    """
    if storage_type == 'db':
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    else:
        text = ""
        place_id = ""
        user_id = ""
