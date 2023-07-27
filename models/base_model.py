#!/usr/bin/python3
"""The BaseModel module
"""
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from uuid import uuid4

if models.storage_type == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """Defines the common attributes/methods for other classes
    """
    if models.storage_type == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = updated_at = Column(DateTime, nullable=False,
                                         default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Runs when a new instance is created
        """
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

        else:
            if "id" not in kwargs:
                self.id = str(uuid4())
            if "created_at" not in kwargs:
                self.created_at = self.updated_at = datetime.utcnow()

            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.fromisoformat(value)
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance
        """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when the instance is modified
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance's
        __dict__ attribute
        """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()

        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
        return new_dict

    def delete(self):
        """Delete the current instance from the storage
        """
        models.storage.delete(self)
