#!/usr/bin/python3
"""Tests the command interpreter
"""
from console import HBNBCommand
from io import StringIO
from models import storage
import os

import sys
import unittest
from unittest.mock import patch


class TestConsole(unittest.TestCase):
    """Test the console module
    """
    @classmethod
    def setUpClass(cls):
        """Sets up the class
        """
        storage._FileStorage__file_path = "test.json"

    def setUp(self):
        """Sets up each test
        """
        self.cns = HBNBCommand()
        storage._FileStorage__objects = {}
        if os.path.exists("test.json"):
            os.remove("test.json")

    @unittest.skipUnless(sys.__stdin__.isatty(), "interactive mode only")
    def test_prompt(self):
        """Test the prompt
        """
        self.assertEqual("(hbnb) ", self.cns.prompt)

    def test_help(self):
        """Test the help command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("help quit")
            output = "Exits the program\n"
            self.assertEqual(output, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("help EOF")
            output = "Exits the program on receiving the EOF signal\n"
            self.assertEqual(output, f.getvalue())

    def test_emptyline(self):
        """Test an empty line input
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("\n")
            self.assertEqual("", f.getvalue())

    def test_quit(self):
        """Test the quit command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("quit")
            self.assertEqual("", f.getvalue())

    def test_EOF(self):
        """Test the EOF command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("EOF")
            self.assertEqual("\n", f.getvalue())

    def test_create(self):
        """Test the create command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create BaseModel")
            self.assertEqual(36, len(f.getvalue().strip()))
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create User")
            self.assertEqual(36, len(f.getvalue().strip()))

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd('create State name="California"')
            self.assertEqual(36, len(f.getvalue().strip()))
            self.cns.onecmd('show State ' + f.getvalue().strip())
            self.assertIn("'name': 'California'", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            params = ('city_id="0001" user_id="0001" name="My_little_house" '
                      'number_rooms=4 number_bathrooms=2 max_guest=10 '
                      'price_by_night=300 latitude=37.773972 '
                      'longitude=-122.431297')
            self.cns.onecmd('create Place ' + params)
            self.assertEqual(36, len(f.getvalue().strip()))
            self.cns.onecmd('show Place ' + f.getvalue().strip())
            self.assertIn("'city_id': '0001'", f.getvalue())
            self.assertIn("'user_id': '0001'", f.getvalue())

            self.assertIn("'name': 'My little house'", f.getvalue())
            self.assertIn("'number_rooms': 4", f.getvalue())
            self.assertIn("'number_bathrooms': 2", f.getvalue())

            self.assertIn("'max_guest': 10", f.getvalue())
            self.assertIn("'price_by_night': 300", f.getvalue())
            self.assertIn("'latitude': 37.773972", f.getvalue())
            self.assertIn("'longitude': -122.431297", f.getvalue())

    def test_show(self):
        """Test the show command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("show")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("show MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("show BaseModel")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("show BaseModel 123456-abcdef-123456")
            self.assertEqual("** no instance found **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create BaseModel")
            key = "BaseModel." + f.getvalue().strip()
            self.cns.onecmd("show BaseModel " + f.getvalue().strip())
            self.assertIn(str(storage.all()[key]) + "\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create User")
            key = "User." + f.getvalue().strip()
            self.cns.onecmd("show User " + f.getvalue().strip())
            self.assertIn(str(storage.all()[key]) + "\n", f.getvalue())

    def test_destroy(self):
        """Test the destroy command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("destroy")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("destroy MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("destroy BaseModel")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("destroy BaseModel 123456-abcdef-123456")
            self.assertEqual("** no instance found **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create BaseModel")
            key = "BaseModel." + f.getvalue().strip()
            self.cns.onecmd("destroy BaseModel " + f.getvalue().strip())
            self.assertNotIn(key, storage.all())

    def test_all(self):
        """Test the all command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("all MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        # Test the all command with no objects
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("all")
            self.assertEqual("[]\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create BaseModel")
            self.cns.onecmd("create User")
            self.cns.onecmd("create Place")
            self.cns.onecmd("all BaseModel")

            self.assertIn("BaseModel", f.getvalue())
            self.assertNotIn("User", f.getvalue())
            self.assertNotIn("Place", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create BaseModel")
            self.cns.onecmd("create User")
            self.cns.onecmd("create Place")
            self.cns.onecmd("all User")

            self.assertNotIn("BaseModel", f.getvalue())
            self.assertIn("User", f.getvalue())
            self.assertNotIn("Place", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create BaseModel")
            self.cns.onecmd("create User")
            self.cns.onecmd("create Place")
            self.cns.onecmd("all")

            self.assertIn("BaseModel", f.getvalue())
            self.assertIn("User", f.getvalue())
            self.assertIn("Place", f.getvalue())

    def test_update(self):
        """Test the update command
        """
        object_id = ""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("update")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("update MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("update BaseModel")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("update BaseModel 123456-abcdef-123456")
            self.assertEqual("** no instance found **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("create BaseModel")
            object_id = f.getvalue().strip()
            self.cns.onecmd("update BaseModel " + object_id)
            self.assertIn("** attribute name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("update BaseModel " + object_id +
                                " first_name")
            self.assertEqual("** value missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("update BaseModel " + object_id +
                                " first_name \"Betty\"")
            self.assertEqual("", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("show BaseModel " + object_id)
            self.assertIn("Betty", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("update BaseModel " + object_id +
                                " first_name \"Holberton\"")
            self.assertEqual("", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cns.onecmd("show BaseModel " + object_id)
            self.assertIn("Holberton", f.getvalue())
