#!/usr/bin/python3
"""Module for testing the DBStorage class
"""
import os
import unittest
from uuid import uuid4

import MySQLdb

from models.amenity import Amenity
from models.city import City
from models.engine import db_storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

db_condition = (os.getenv('HBNB_ENV') == 'test'
                and os.getenv('HBNB_TYPE_STORAGE') == 'db')


@unittest.skipUnless(db_condition, "Testing DBStorage only")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    MODEL_TABLES = (
        (State, "states"),
        (User, "users"),
        (City, "cities"),
        (Place, "places"),
        (Amenity, "amenities"),
        (Review, "reviews"),
    )

    @classmethod
    def setUpClass(cls):
        """Set up database connection for test class"""
        cls.db_conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            user=os.getenv('HBNB_MYSQL_USER', 'hbnb_test'),
            passwd=os.getenv('HBNB_MYSQL_PWD', 'hbnb_test_pwd'),
            db=os.getenv('HBNB_MYSQL_DB', 'hbnb_test_db')
        )
        cls.db_cursor = cls.db_conn.cursor()
        cls.storage = db_storage.DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Close database connection after test class"""
        cls.db_cursor.close()
        cls.db_conn.close()
        cls.storage.close()

    def _get_table_row_count(self, table_name):
        """Helper method to get the count of rows in a table.

        Args:
            table_name (str): The name of the table to count rows in

        Returns:
            int: The number of rows in the table
        """
        self.db_conn.commit()
        self.db_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        result = self.db_cursor.fetchone()
        return result[0] if result else 0

    def _get_row_by_id(self, table_name, row_id):
        """Helper method to retrieve a specific row by id.

        Args:
            table_name (str): The name of the table
            row_id (str): The id to search for

        Returns:
            tuple: The row data or None if not found
        """
        self.db_conn.commit()
        self.db_cursor.execute(
            f"SELECT * FROM {table_name} WHERE id = %s",
            (row_id,)
        )
        return self.db_cursor.fetchone()

    def _get_user_email_by_id(self, user_id):
        """Helper method to retrieve a user's email by id."""
        self.db_conn.commit()
        self.db_cursor.execute(
            "SELECT email FROM users WHERE id = %s",
            (user_id,)
        )
        result = self.db_cursor.fetchone()
        return result[0] if result else None

    def _count_tables(self, table_names=None):
        """Return a mapping of table names to row counts."""
        if table_names is None:
            table_names = [table for _, table in self.MODEL_TABLES]
        return {
            table_name: self._get_table_row_count(table_name)
            for table_name in table_names
        }

    def _build_related_objects(self, prefix="Test"):
        """Build related model instances for integration tests."""
        token = uuid4().hex[:8]
        state = State(name=f"{prefix}State{token}")
        user = User(
            email=f"{prefix.lower()}.{token}@example.com",
            password="password123",
            first_name=prefix,
            last_name="User"
        )
        city = City(name=f"{prefix}City{token}", state_id=state.id)
        place = Place(
            name=f"{prefix}Place{token}",
            city_id=city.id,
            user_id=user.id,
            description=f"{prefix} place for testing",
            number_rooms=2,
            number_bathrooms=1,
            max_guest=4,
            price_by_night=100
        )
        amenity = Amenity(name=f"{prefix}Amenity{token}")
        review = Review(
            text=f"{prefix} review",
            place_id=place.id,
            user_id=user.id
        )
        return {
            State: state,
            User: user,
            City: city,
            Place: place,
            Amenity: amenity,
            Review: review,
        }

    def _persist_objects(self, objects):
        """Add multiple objects to the session and commit once."""
        for obj in objects:
            self.storage.new(obj)
        self.storage.save()

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_all_no_class_returns_all_types(self):
        """Test that all() returns all objects of all types when no class
        is specified.
        """
        initial_counts = self._count_tables()
        created_objects = self._build_related_objects(prefix="AllTypes")
        self._persist_objects(created_objects.values())

        all_objects = self.storage.all()

        for obj in created_objects.values():
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.assertIn(key, all_objects)

        # Verify database has the new records
        final_counts = self._count_tables()
        num_created = len(created_objects)
        self.assertEqual(
            sum(final_counts.values()),
            sum(initial_counts.values()) + num_created,
            f"Database should have {num_created} more records after save()"
        )

        for _, table_name in self.MODEL_TABLES:
            self.assertEqual(
                final_counts[table_name],
                initial_counts[table_name] + 1,
                f"Table {table_name} should have one additional row"
            )

    def test_new_adds_object_to_session(self):
        """Test that new() adds an object to the session.
        """
        new_state = State(name="SessionTest")
        self.storage.new(new_state)

        all_objects = self.storage.all()
        key = f"State.{new_state.id}"
        self.assertIn(key, all_objects,
                      "New object should be in session after new() call")

        db_state = self._get_row_by_id("states", new_state.id)
        self.assertIsNone(
            db_state,
            "New object should NOT be in database without save()"
        )

        # Clean up by saving for other tests
        self.storage.save()

    def test_save_persists_to_database(self):
        """Test that save() commits objects to the database.
        """
        initial_count = self._get_table_row_count("users")

        new_user = User(
            email="savetest@example.com",
            password="testpwd123",
            first_name="Save",
            last_name="Test"
        )
        self.storage.new(new_user)
        self.storage.save()

        final_count = self._get_table_row_count("users")
        self.assertEqual(final_count, initial_count + 1,
                         "Database should have one more user after save()")

        # Verify the specific user record exists in database
        saved_email = self._get_user_email_by_id(new_user.id)
        self.assertIsNotNone(saved_email, "User should exist in database")
        self.assertEqual(
            saved_email,
            "savetest@example.com",
            "User email should be persisted in database"
        )

    def test_all_with_class_filter(self):
        """Test that all(cls) returns only objects of specified class.
        """
        created_objects = self._build_related_objects(prefix="Filter")
        self._persist_objects(created_objects.values())

        for cls, _ in self.MODEL_TABLES:
            class_objects = self.storage.all(cls)
            name = cls.__name__
            for key, obj in class_objects.items():
                self.assertIsInstance(
                    obj, cls,
                    f"all({name}) should only return {name} objects"
                )
                self.assertTrue(
                    key.startswith(f"{name}."),
                    f"{name} key should start with '{name}.'"
                )

            created_key = f"{name}.{created_objects[cls].id}"
            self.assertIn(
                created_key,
                class_objects,
                f"all({name}) should include newly saved {name} object"
            )

    def test_delete_with_none_does_not_change_database(self):
        """Test that delete(None) is a safe no-op."""
        table_names = [table_name for _, table_name in self.MODEL_TABLES]
        initial_counts = self._count_tables(table_names)

        self.storage.delete(None)
        self.storage.save()

        final_counts = self._count_tables(table_names)
        self.assertEqual(
            final_counts,
            initial_counts,
            "delete(None) should not change database row counts"
        )

    def test_delete_removes_object_after_save(self):
        """Test that delete(obj) removes object from DB after save()."""
        token = uuid4().hex[:8]
        user = User(
            email=f"delete.{token}@example.com",
            password="deletepwd123",
            first_name="Delete",
            last_name="Test"
        )
        self.storage.new(user)
        self.storage.save()

        self.assertIsNotNone(
            self._get_row_by_id("users", user.id),
            "User should exist in database before delete()"
        )

        self.storage.delete(user)

        self.assertIsNotNone(
            self._get_row_by_id("users", user.id),
            "User should still exist in database until save() commits delete"
        )

        self.storage.save()

        self.assertIsNone(
            self._get_row_by_id("users", user.id),
            "User should be removed from database after delete() and save()"
        )
