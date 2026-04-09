#!/usr/bin/python3
"""
This module consists of all the possible test
conditions for the class `State` class
"""
import datetime
import unittest

import pycodestyle

import models
from models.base_model import BaseModel
from models.state import State


class StateTest(unittest.TestCase):
    """This test class contains all test methods """

    def test_instance(self):
        """Check proper instance is created """
        new_state = State()
        self.assertIsInstance(new_state, State)

    def test_subclass(self):
        """Make sure State class is a subclass of BaseModel class """
        self.assertEqual(True, issubclass(State, BaseModel))

    def test_class_attribute(self):
        """Check all class attributes """
        new_state = State(name="California")
        self.assertEqual(new_state.name, "California")

    def test_attribute_exist(self):
        """Make sure attributes exist """
        new_state = State()
        self.assertTrue(hasattr(new_state, 'name'))
        self.assertTrue(hasattr(new_state, 'id'))
        self.assertTrue(hasattr(new_state, 'created_at'))
        self.assertTrue(hasattr(new_state, 'updated_at'))

    def test_class_attribute_pass_value(self):
        """Check all class attributes """
        new_state = State()
        new_state.name = "Betty"

        self.assertEqual(new_state.name, "Betty")

    def test_has_right_attributes(self):
        """Make sure if the type of the attribute is the right one"""
        new_state = State(name="California")
        self.assertIsInstance(new_state.name, str)
        self.assertIsInstance(new_state.id, str)
        self.assertIsInstance(new_state.created_at, datetime.datetime)
        self.assertIsInstance(new_state.updated_at, datetime.datetime)

    def test_doc(self):
        """Check documentation """
        self.assertIsNotNone(models.state.__doc__)  # type: ignore
        self.assertIsNotNone(State.__doc__)

    def test_pycodestyle(self):
        """Check PEP 8 style """
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors.")
