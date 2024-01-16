#!/usr/bin/python3
"""This module defines a class User."""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """
    User class inherits from BaseModel and Base.

    The User class represents a user in the HBNB project. In a database setup,
    User objects are stored in the 'users' table.

    Attributes:
        id (str): Unique identifier for the User.
        created_at (datetime): The datetime when the User instance was created.
        updated_at (datetime): The datetime when the User instance
                was last updated.
        email (str): The email address of the User.
        password (str): The password of the User.
        first_name (str): The first name of the User.
        last_name (str): The last name of the User.
        places (relationship): One-to-many relationship with the Place class,
                representing places associated with the user.
        reviews (relationship): One-to-many relationship with the Review class,
                representing reviews associated with the user.
    """

    __tablename__ = "users"
    email = (
        Column(String(128), nullable=False)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )

    password = (
        Column(String(128), nullable=False)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )

    first_name = (
        Column(String(128), nullable=True)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )

    last_name = (
        Column(String(128), nullable=True)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )

    places = (
        relationship(
            "Place", cascade="all, delete, delete-orphan", backref="user"
        )
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else None
    )

    reviews = (
        relationship(
            "Review", cascade="all, delete, delete-orphan", backref="user"
        )
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else None
    )
