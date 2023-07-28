#!/usr/bin/python3
"""The user module
"""
from .base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Defines the attributes of a user, inherits from BaseModel and
    Base (SQLAlchemy)

    Attributes:
        email (str): The user's email address
        password (str): The user's password
        first_name (str): The user's first name
        last_name (str): The user's last name

        places (list): The list of Place objects linked to the user (db only)
    """
    if storage_type == 'db':
        __tablename__ = 'users'
        __table_args__ = {'mysql_default_charset': 'latin1'}
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)

        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user", cascade="all, delete")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete")

    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
