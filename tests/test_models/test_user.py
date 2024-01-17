#!/usr/bin/python3
"""Defines the unittests for the User model."""
import os
from tests.test_models.test_base_model import test_basemodel
from models.user import User
import unittest


class test_user(test_basemodel):
    """A unittest for User class."""

    def __init__(self, *args, **kwargs):
        """Initialize the test class for User."""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """Tests the type of first_name attribute."""
        new = self.value()
        self.assertEqual(
            type(new.first_name),
            str if os.getenv("HBNB_TYPE_STORAGE") != "db" else type(None),
        )

    def test_last_name(self):
        """Tests the type of last_name attribute."""
        new = self.value()
        self.assertEqual(
            type(new.last_name),
            str if os.getenv("HBNB_TYPE_STORAGE") != "db" else type(None),
        )

    def test_email(self):
        """Tests the type of email attribute."""
        new = self.value()
        self.assertEqual(
            type(new.email),
            str if os.getenv("HBNB_TYPE_STORAGE") != "db" else type(None),
        )

    def test_password(self):
        """Tests the type of password attribute."""
        new = self.value()
        self.assertEqual(
            type(new.password),
            str if os.getenv("HBNB_TYPE_STORAGE") != "db" else type(None),
        )


if __name__ == "__main__":
    unittest.main()
