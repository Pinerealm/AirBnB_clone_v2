#!/usr/bin/python3
""" Module for testing file storage"""
import json
import os
import unittest

from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.state import State


class TestFileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    @classmethod
    def setUpClass(cls):
        """Sets up the class
        """
        FileStorage._FileStorage__file_path = "test.json"  # type: ignore

    def setUp(self):
        """ Set up for each test """
        self.fstore = FileStorage()
        self.fstore.all().clear()
        if os.path.exists("test.json"):
            os.remove("test.json")

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(self.fstore.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        self.fstore.new(new)
        key = new.__class__.__name__ + '.' + new.id
        self.assertIn(key, self.fstore.all())

        new2 = State()
        self.fstore.new(new2)
        key2 = new2.__class__.__name__ + '.' + new2.id
        self.assertIn(key2, self.fstore.all())

    def test_all(self):
        """ __objects is properly returned """
        new = State()
        before = self.fstore.all().copy()
        self.fstore.new(new)

        after = self.fstore.all()
        self.assertNotEqual(before, after)
        self.assertDictEqual(self.fstore.all(), after)

    def test_all_with_cls(self):
        """ __objects is properly filtered by class """
        new = State()
        self.fstore.new(new)
        new2 = City()
        self.fstore.new(new2)

        state_objs = self.fstore.all(State)
        self.assertIn(new.__class__.__name__ + '.' + new.id, state_objs)
        self.assertNotIn(new2.__class__.__name__ + '.' + new2.id, state_objs)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        self.fstore.new(new)
        self.fstore.save()
        self.assertTrue(os.path.exists('test.json'))

        key = "{}.{}".format(new.__class__.__name__, new.id)
        with open('test.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertIn(key, data)
            self.assertEqual(data[key]['id'], new.id)
            self.assertEqual(data[key]['__class__'], 'BaseModel')

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        self.fstore.new(new)
        self.fstore.save()
        self.fstore.reload()

        key = "{}.{}".format(new.__class__.__name__, new.id)
        self.assertIn(key, self.fstore.all())
        self.assertEqual(self.fstore.all()[key].id, new.id)
        self.assertEqual(
            self.fstore.all()[key].__class__.__name__, 'BaseModel'
        )

    def test_reload_empty(self):
        """ Load from an empty file (no error expected) """
        with open('test.json', 'w') as f:
            pass
        self.assertEqual(self.fstore.reload(), None)

        with open('test.json', 'w') as f:
            json.dump({}, f)
        self.assertEqual(self.fstore.reload(), None)

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(self.fstore.reload(), None)

    def test_delete(self):
        """Object is deleted from __objects and file on disk
        when delete is called
        """
        new = City()
        self.fstore.new(new)
        self.fstore.save()
        key = "{}.{}".format(new.__class__.__name__, new.id)
        self.assertIn(key, self.fstore.all())

        self.fstore.delete(new)
        self.assertNotIn(key, self.fstore.all())
        with open('test.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertNotIn(key, data)

    def test_close(self):
        """ close() calls reload() """
        new = BaseModel()
        self.fstore.new(new)
        self.fstore.save()
        self.fstore.all().clear()

        self.fstore.close()
        key = "{}.{}".format(new.__class__.__name__, new.id)
        self.assertIn(key, self.fstore.all())

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(
            type(self.fstore._FileStorage__file_path),  # type: ignore
            str
        )

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(self.fstore.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        self.fstore.new(new)
        expected_key = 'BaseModel' + '.' + new.id
        self.assertIn(expected_key, self.fstore.all())
