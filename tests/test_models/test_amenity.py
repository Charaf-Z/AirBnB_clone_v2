#!/usr/bin/python3
"""This module instantiates an object of storage engine."""
import os
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
import unittest


class test_amenity(test_basemodel):
    """Test the Amenity class and its methods."""

    def __init__(self, *args, **kwargs):
        """Initialize the test class for Amenity."""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Tests the type of name attribute."""
        new = self.value()
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            self.assertNotEqual(type(new.name), str)
        else:
            self.assertEqual(type(new.name), type(None))


if __name__ == "__main__":
    unittest.main()
