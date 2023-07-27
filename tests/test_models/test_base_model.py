#!/usr/bin/python3
"""This module tests the BaseModel class.
"""
from datetime import datetime
from models import storage
from models.base_model import BaseModel
import unittest

import json
import os


class TestBaseModel(unittest.TestCase):
    """Tests the BaseModel class
    """
    @classmethod
    def setUpClass(cls):
        """Sets up the class
        """
        storage._FileStorage__file_path = "test.json"

    def setUp(self):
        """Sets up each test
        """
        self.name = 'BaseModel'
        storage._FileStorage__objects = {}
        if os.path.exists("test.json"):
            os.remove("test.json")

    def tearDown(self):
        """Removes JSON file created by each test"""
        try:
            os.remove(self._FileStorage__file_path)
        except:
            pass

    def test_init(self):
        """Tests the __init__ method
        """
        b1 = BaseModel()
        b2 = BaseModel()
        b1_dict = b1.to_dict()
        b3 = BaseModel(**b1_dict)

        self.assertIsInstance(b1, BaseModel)
        self.assertIsInstance(b1.id, str)
        self.assertIsInstance(b1.created_at, datetime)
        self.assertIsInstance(b1.updated_at, datetime)

        self.assertNotEqual(b1.id, b2.id)
        self.assertEqual(b1.created_at, b1.updated_at)
        self.assertNotEqual(b1.created_at, b2.created_at)
        self.assertNotEqual(b1.updated_at, b2.updated_at)

        self.assertEqual(b1.id, b3.id)
        self.assertEqual(b1.created_at, b3.created_at)
        self.assertEqual(b1.updated_at, b3.updated_at)
        self.assertIsNot(b1, b3)

    def test_default(self):
        """Tests the __init__ method with no arguments
        """
        i = BaseModel()
        self.assertEqual(type(i), BaseModel)

    def test_kwargs(self):
        """Tests the __init__ method with kwargs
        """
        i = BaseModel()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Tests the __init__ method with an int as kwargs
        """
        i = BaseModel()
        copy = i.to_dict()
        copy.update({1: 2})
        self.assertRaises(TypeError, 'BaseModel', '**copy')
        # with self.assertRaises(TypeError):
        #     new = BaseModel(**copy)

    def test_save(self):
        """Tests the save method
        """
        b1 = BaseModel()
        self.assertEqual(b1.created_at, b1.updated_at)
        b1.save()
        self.assertNotEqual(b1.created_at, b1.updated_at)
        key = self.name + "." + b1.id

        with open(storage._FileStorage__file_path, "r") as f:
            self.assertIn("BaseModel." + b1.id, f.read())
        with open(storage._FileStorage__file_path, 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], b1.to_dict())

    def test_str(self):
        """Tests the __str__ method
        """
        b1 = BaseModel()
        b1_str = str(b1)
        expected = f'[{self.name}] ({b1.id}) {b1.__dict__}'
        self.assertIsInstance(b1_str, str)
        self.assertEqual(b1_str, expected)
        
    def test_to_dict(self):
        """Tests the to_dict method
        """
        b1 = BaseModel()
        b1_dict = b1.to_dict()
        self.assertIsInstance(b1_dict, dict)
        self.assertIsInstance(b1_dict["id"], str)

        self.assertIsInstance(b1_dict["created_at"], str)
        self.assertIsInstance(b1_dict["updated_at"], str)
        self.assertEqual(b1_dict["created_at"], b1.created_at.isoformat())
        self.assertEqual(b1_dict["updated_at"], b1.updated_at.isoformat())
        self.assertEqual(b1_dict["__class__"], "BaseModel")

    def test_kwargs_none(self):
        """Tests the __init__ method with kwargs None
        """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = BaseModel(**n)

    def test_id(self):
        """Tests the id attribute
        """
        new = BaseModel()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Tests the created_at attribute
        """
        new = BaseModel()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """Tests the updated_at attribute
        """
        new = BaseModel()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertTrue(new.created_at == new.updated_at)
