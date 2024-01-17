#!/usr/bin/python3
"""Defines the unittests for the City model."""
import unittest
import os
from models.city import City
from tests.test_models.test_base_model import test_basemodel


class test_city(test_basemodel):
    """A unittest for City class."""

    def __init__(self, *args, **kwargs):
        """Initialize the test class for City."""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Tests the type of state_id attribute."""
        new = self.value()
        self.assertEqual(
            type(new.state_id),
            str if os.getenv("HBNB_TYPE_STORAGE") != "db" else type(None),
        )

    def test_name(self):
        """Tests the type of name attribute."""
        new = self.value()
        self.assertEqual(
            type(new.name),
            str if os.getenv("HBNB_TYPE_STORAGE") != "db" else type(None),
        )


if __name__ == "__main__":
    unittest.main()
