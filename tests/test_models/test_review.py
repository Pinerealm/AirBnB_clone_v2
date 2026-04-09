#!/usr/bin/python3
"""
This module consists of all the possible test
conditions for the class `Review` class
"""
import datetime
import unittest

import pycodestyle

import models
from models.base_model import BaseModel
from models.review import Review


class ReviewTest(unittest.TestCase):
    """This test class contains all test methods """

    def test_instance(self):
        """Check proper instance is created """
        new_review = Review()
        self.assertIsInstance(new_review, Review)

    def test_subclass(self):
        """Make sure User class is a subclass of BaseModel class """
        self.assertEqual(True, issubclass(Review, BaseModel))

    def test_class_attribute(self):
        """Check all class attributes """
        new_review = Review(text="Amazing place to stay",
                            place_id="123456", user_id="123456")
        self.assertEqual(new_review.place_id, "123456")
        self.assertEqual(new_review.user_id, "123456")
        self.assertEqual(new_review.text, "Amazing place to stay")

    def test_attribute_exist(self):
        """Make sure attributes exist """
        new_review = Review()
        self.assertTrue(hasattr(new_review, 'place_id'))
        self.assertTrue(hasattr(new_review, 'user_id'))
        self.assertTrue(hasattr(new_review, 'text'))
        self.assertTrue(hasattr(new_review, 'id'))
        self.assertTrue(hasattr(new_review, 'created_at'))
        self.assertTrue(hasattr(new_review, 'updated_at'))

    def test_class_attribute_pass_value(self):
        """Check all class attributes """
        new_review = Review()
        new_review.place_id = "b69b2acf-121e-433c-9634-50ac93a6ce76"
        new_review.user_id = "b69b2acf-121e-433c-9634-50ac93a6ce77"
        new_review.text = "sil"

        self.assertEqual(new_review.place_id,
                         "b69b2acf-121e-433c-9634-50ac93a6ce76")
        self.assertEqual(new_review.user_id,
                         "b69b2acf-121e-433c-9634-50ac93a6ce77")
        self.assertEqual(new_review.text, "sil")

    def test_has_right_attributes(self):
        """Make sure if the type of the attribute is the right one"""
        new_review = Review(text="Amazing place to stay",
                            place_id="123456", user_id="123456")
        self.assertIsInstance(new_review.place_id, str)
        self.assertIsInstance(new_review.user_id, str)
        self.assertIsInstance(new_review.text, str)
        self.assertIsInstance(new_review.id, str)
        self.assertIsInstance(new_review.created_at, datetime.datetime)
        self.assertIsInstance(new_review.updated_at, datetime.datetime)

    def test_doc(self):
        """Check documentation """
        self.assertIsNotNone(models.review.__doc__)  # type: ignore
        self.assertIsNotNone(Review.__doc__)

    def test_pycodestyle(self):
        """Check PEP 8 style """
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors.")
