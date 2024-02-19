#!/usr/bin/python3
"""Review module for the HBNB project."""
import os
from sqlalchemy import Column, ForeignKey, String
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """
    Review class to store review information.

    The Review class inherits from BaseModel and is used to represent reviews
            in the HBNB project. In a database setup,
            Review objects are stored in the 'reviews' table.

    Attributes:
        id (str): Unique identifier for the Review.
        created_at (datetime): The datetime when the Review instance
                was created.
        updated_at (datetime): The datetime when the Review instance
                was last updated.
        place_id (str): The foreign key linking the Review to a Place.
        user_id (str): The foreign key linking the Review to a User.
        text (str): The content of the review.
    """

    __tablename__ = "reviews"
    place_id = (
        Column(String(60), ForeignKey("places.id"), nullable=False)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )
    user_id = (
        Column(String(60), ForeignKey("users.id"), nullable=False)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )
    text = (
        Column(String(1024), nullable=False)
        if os.getenv("HBNB_TYPE_STORAGE") == "db"
        else ""
    )
