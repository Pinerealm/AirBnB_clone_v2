#!/usr/bin/python3
"""
This module tests the `Place` class
"""
import datetime
import unittest

import pycodestyle

import models
from models.base_model import BaseModel
from models.place import Place


class PlaceTest(unittest.TestCase):
    """This test class contains all test methods """

    def test_instance(self):
        """Check proper instance is created """
        user1 = Place()
        self.assertIsInstance(user1, Place)

    def test_subclass(self):
        """Make sure Place class is a subclass of BaseModel class """
        self.assertEqual(True, issubclass(Place, BaseModel))

    def test_class_attribute(self):
        """Check all class attributes """
        new_place = Place(city_id="12345", user_id="12345",
                          name="Example Place",
                          description="A beautiful place",
                          number_rooms=3, number_bathrooms=2,
                          max_guest=5, price_by_night=100,
                          latitude=40.712776, longitude=-74.005974)
        self.assertEqual(new_place.city_id, "12345")
        self.assertEqual(new_place.user_id, "12345")
        self.assertEqual(new_place.name, "Example Place")
        self.assertEqual(new_place.description, "A beautiful place")
        self.assertEqual(new_place.number_rooms, 3)
        self.assertEqual(new_place.number_bathrooms, 2)
        self.assertEqual(new_place.max_guest, 5)
        self.assertEqual(new_place.price_by_night, 100)
        self.assertEqual(new_place.latitude, 40.712776)
        self.assertEqual(new_place.longitude, -74.005974)

        if models.storage_type != 'db':
            self.assertEqual(new_place.amenity_ids, [])

    def test_attribute_exist(self):
        """Make sure attributes exist """
        new_place = Place(city_id="12345", user_id="12345",
                          name="Example Place")
        self.assertTrue(hasattr(new_place, 'city_id'))
        self.assertTrue(hasattr(new_place, 'user_id'))
        self.assertTrue(hasattr(new_place, 'name'))
        self.assertTrue(hasattr(new_place, 'description'))
        self.assertTrue(hasattr(new_place, 'number_rooms'))
        self.assertTrue(hasattr(new_place, 'number_bathrooms'))
        self.assertTrue(hasattr(new_place, 'max_guest'))
        self.assertTrue(hasattr(new_place, 'price_by_night'))
        self.assertTrue(hasattr(new_place, 'latitude'))
        self.assertTrue(hasattr(new_place, 'longitude'))

        if models.storage_type != 'db':
            self.assertTrue(hasattr(new_place, 'amenity_ids'))

    def test_class_attribute_pass_value(self):
        """Check all class attributes """
        new_place = Place()
        new_place.city_id = "66d0dd7c-9336-49b5-93f7-0cfcc0f6f1d2"
        new_place.user_id = "66d0dd7c-9336-49b5-93f7-0cfcc0f6f1d6"
        new_place.name = "airmail"
        new_place.description = "root"
        new_place.number_rooms = 300
        new_place.number_bathrooms = 300
        new_place.max_guest = 100
        new_place.price_by_night = 180
        new_place.latitude = 51.507351
        new_place.longitude = -0.127758
        new_place.amenity_ids = ["66d0dd7c-9336-49b5-93f7-0cfcc0f6f1d10"]

        self.assertEqual(new_place.city_id,
                         "66d0dd7c-9336-49b5-93f7-0cfcc0f6f1d2")
        self.assertEqual(new_place.user_id,
                         "66d0dd7c-9336-49b5-93f7-0cfcc0f6f1d6")
        self.assertEqual(new_place.name, "airmail")
        self.assertEqual(new_place.description, "root")
        self.assertEqual(new_place.number_rooms, 300)
        self.assertEqual(new_place.number_bathrooms, 300)
        self.assertEqual(new_place.max_guest, 100)
        self.assertEqual(new_place.price_by_night, 180)
        self.assertEqual(new_place.latitude, 51.507351)
        self.assertEqual(new_place.longitude, -0.127758)
        self.assertEqual(new_place.amenity_ids,
                         ["66d0dd7c-9336-49b5-93f7-0cfcc0f6f1d10"])

    def test_has_right_attributes(self):
        """Make sure if the type of the attribute is the right one"""
        new_place = Place(city_id="12345", user_id="12345",
                          description="A beautiful place",
                          name="Example Place",
                          number_rooms=3, number_bathrooms=2,
                          max_guest=5,
                          price_by_night=100, latitude=40.712776,
                          longitude=-74.005974,
                          amenity_ids=["12345"])
        self.assertIsInstance(new_place.city_id, str)
        self.assertIsInstance(new_place.user_id, str)
        self.assertIsInstance(new_place.name, str)
        self.assertIsInstance(new_place.description, str)
        self.assertIsInstance(new_place.number_rooms, int)
        self.assertIsInstance(new_place.number_bathrooms, int)
        self.assertIsInstance(new_place.max_guest, int)
        self.assertIsInstance(new_place.price_by_night, int)
        self.assertIsInstance(new_place.latitude, float)
        self.assertIsInstance(new_place.longitude, float)
        self.assertIsInstance(new_place.amenity_ids, list)
        self.assertIsInstance(new_place.created_at, datetime.datetime)
        self.assertIsInstance(new_place.updated_at, datetime.datetime)

    def test_doc(self):
        """Check documentation """
        self.assertIsNotNone(models.place.__doc__)  # type: ignore
        self.assertIsNotNone(Place.__doc__)

    def test_pycodestyle(self):
        """Check PEP 8 style """
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors.")
