#!/usr/bin/python3
""" Place Module for HBNB project """
from .base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship

if storage_type == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """The place class 
    """
    if storage_type == 'db':
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey('cities.id'),
                         nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'),
                         nullable=False)
        
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)

        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 back_populates="place_amenities",
                                 viewonly=False)
        

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """ Gets the list of reviews associated with the current place.
            """
            from .review import Review
            from models import storage

            review_list = []
            for value in storage.all(Review).values():
                if value.place_id == self.id:
                    review_list.append(value)
            return review_list

        @property
        def amenities(self):
            """ Gets the list of amenities associated with the current place.
            """
            from .amenity import Amenity
            from models import storage

            amenity_list = []
            for value in storage.all(Amenity).values():
                if value.id in self.amenity_ids:
                    amenity_list.append(value)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """Adds an amenity id to the amenity_ids list.
            """
            from .amenity import Amenity

            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
