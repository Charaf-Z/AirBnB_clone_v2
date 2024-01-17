#!/usr/bin/python3
"""test for console"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
import console
from console import HBNBCommand


class TestConsole(unittest.TestCase):
    """Test cases for the console modul"""

    @classmethod
    def setUpClass(cls):
        """cases for classes in console"""
        cls.consol = HBNBCommand()

    @classmethod
    def teardown(cls):
        """Tests cases for destroying a class"""
        del cls.consol

    def tearDown(self):
        """test cases for destroynig an instance"""
        if (os.getenv('HBNB_TYPE_STORAGE') != 'db'):
            try:
                os.remove("file.json")
            except Exception:
                pass

    def test_docstrings_in_console(self):
        """Test cases for docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)

    def test_emptyline(self):
        """Test Cases empty line"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("\n")
            self.assertEqual('', f.getvalue())


if __name__ == "__main__":
    unittest.main()
