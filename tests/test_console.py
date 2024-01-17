#!/usr/bin/python3
"""A unit test module for the console module."""
import os
import unittest
from io import StringIO
from unittest.mock import patch
import MySQLdb
import sqlalchemy
import pep8
import console
from console import HBNBCommand
from models import storage
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    """A class for testing the console module."""

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_fs_create(self):
        """Tests the create command with the file storage."""
        with patch("sys.stdout", new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City name="Texas"')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn("City.{}".format(mdl_id), storage.all().keys())
            cons.onecmd("show City {}".format(mdl_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            clear_stream(cout)
            cons.onecmd('create User name="James" age=17 height=5.9')
            mdl_id = cout.getvalue().strip()
            self.assertIn("User.{}".format(mdl_id), storage.all().keys())
            clear_stream(cout)
            cons.onecmd("show User {}".format(mdl_id))
            self.assertIn("'name': 'James'", cout.getvalue().strip())
            self.assertIn("'age': 17", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage test")
    def test_db_create(self):
        """Tests the create command with the database storage."""
        with patch("sys.stdout", new=StringIO()) as cout:
            cons = HBNBCommand()
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cons.onecmd("create User")
            clear_stream(cout)
            cons.onecmd('create User email="john25@gmail.com" password="123"')
            mdl_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv("HBNB_MYSQL_HOST"),
                port=3306,
                user=os.getenv("HBNB_MYSQL_USER"),
                passwd=os.getenv("HBNB_MYSQL_PWD"),
                db=os.getenv("HBNB_MYSQL_DB"),
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn("john25@gmail.com", result)
            self.assertIn("123", result)
            cursor.close()
            dbc.close()

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage test")
    def test_db_show(self):
        """Tests the show command with the database storage."""
        with patch("sys.stdout", new=StringIO()) as cout:
            cons = HBNBCommand()
            # showing a User instance
            obj = User(email="john25@gmail.com", password="123")
            dbc = MySQLdb.connect(
                host=os.getenv("HBNB_MYSQL_HOST"),
                port=3306,
                user=os.getenv("HBNB_MYSQL_USER"),
                passwd=os.getenv("HBNB_MYSQL_PWD"),
                db=os.getenv("HBNB_MYSQL_DB"),
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            cons.onecmd("show User {}".format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(), "** no instance found **"
            )
            obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv("HBNB_MYSQL_HOST"),
                port=3306,
                user=os.getenv("HBNB_MYSQL_USER"),
                passwd=os.getenv("HBNB_MYSQL_PWD"),
                db=os.getenv("HBNB_MYSQL_DB"),
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            cons.onecmd("show User {}".format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn("john25@gmail.com", result)
            self.assertIn("123", result)
            self.assertIn("john25@gmail.com", cout.getvalue())
            self.assertIn("123", cout.getvalue())
            cursor.close()
            dbc.close()

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage test")
    def test_db_count(self):
        """Tests the count command with the database storage."""
        with patch("sys.stdout", new=StringIO()) as cout:
            cons = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv("HBNB_MYSQL_HOST"),
                port=3306,
                user=os.getenv("HBNB_MYSQL_USER"),
                passwd=os.getenv("HBNB_MYSQL_PWD"),
                db=os.getenv("HBNB_MYSQL_DB"),
            )
            cursor = dbc.cursor()
            cursor.execute("SELECT COUNT(*) FROM states;")
            res = cursor.fetchone()
            prev_count = int(res[0])
            cons.onecmd('create State name="Enugu"')
            clear_stream(cout)
            cons.onecmd("count State")
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            cons.onecmd("count State")
            cursor.close()
            dbc.close()

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage test")
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage test")
    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["tests/test_console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_docstrings_in_console(self):
        """Checking for docstrings."""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Test empty line input."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """Test quit command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("quit")
            self.assertEqual('', f.getvalue())

    def test_create(self):
        """Test create command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            self.assertEqual(
                "[[User]", f.getvalue()[:7])

    def test_show(self):
        """Test show command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_all(self):
        """Test all command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    def test_update(self):
        """Test update command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    def test_z_all(self):
        """Test alternate all command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.all()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.all()")
            self.assertEqual("[]\n", f.getvalue())

    def test_z_count(self):
        """Test count command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("asdfsdfsd.count()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())

    def test_z_show(self):
        """Test alternate show command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("safdsa.show()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("BaseModel.show(abcd-123)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test alternate destroy command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("Galaxy.destroy()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.destroy(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_update(self):
        """Test alternate destroy command inpout."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("sldkfjsl.update()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(12345)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ")")
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual(
                "** value missing **\n", f.getvalue())


if __name__ == "__main__":
    unittest.main()
