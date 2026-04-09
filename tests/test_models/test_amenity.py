#!/usr/bin/python3
"""
This module tests the `Amenity` class
"""
import datetime
import unittest

import pycodestyle

import models
from models.amenity import Amenity
from models.base_model import BaseModel


class AmenityTest(unittest.TestCase):
    """This test class contains all test methods """

    def test_instance(self):
        """Check proper instance is created """
        amenity_obj = Amenity(name="Wifi")
        self.assertIsInstance(amenity_obj, Amenity)

    def test_subclass(self):
        """Make sure Amenity class is a subclass of BaseModel class """
        self.assertEqual(True, issubclass(Amenity, BaseModel))

    def test_class_attribute(self):
        """Check all class attributes """
        amenity_obj = Amenity(name="Wifi")
        self.assertEqual(amenity_obj.name, "Wifi")

    def test_attribute_exist(self):
        """Make sure attributes exist """
        amenity_obj = Amenity(name="Wifi")
        self.assertTrue(hasattr(amenity_obj, 'name'))
        self.assertTrue(hasattr(amenity_obj, 'id'))
        self.assertTrue(hasattr(amenity_obj, 'created_at'))
        self.assertTrue(hasattr(amenity_obj, 'updated_at'))

    def test_class_attribute_pass_value(self):
        """Check all class attributes """
        amenity_obj = Amenity(name="Television")
        self.assertEqual(amenity_obj.name, "Television")

    def test_has_right_attributes(self):
        """Make sure if the type of the attribute is the right one"""
        amenity_obj = Amenity(name="Wifi")
        self.assertIsInstance(amenity_obj.name, str)
        self.assertIsInstance(amenity_obj.id, str)
        self.assertIsInstance(amenity_obj.created_at, datetime.datetime)
        self.assertIsInstance(amenity_obj.updated_at, datetime.datetime)

    def test_doc(self):
        """Check documentation """
        self.assertIsNotNone(models.amenity.__doc__)  # type: ignore
        self.assertIsNotNone(Amenity.__doc__)

    def test_pycodestyle(self):
        """Check PEP 8 style """
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors.")
