#!/usr/bin/python3
"""City Module for HBNB project."""
import os
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """
    City class representation.

    The City class inherits from BaseModel and is used to represent cities
    in the HBNB project. In a database setup, City objects are stored
    in the 'cities' table.

    Attributes:
        id (str): Unique identifier for the City.
        created_at (datetime): The datetime when the City instance was created.
        updated_at (datetime): The datetime when the City instance
                was last updated.
        state_id (str): The foreign key linking the City to a State.
        name (str): The name of the City.
        places (relationship): One-to-many relationship with the Place class,
                representing places associated with the city.
    """

    __tablename__ = "cities"

    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)
    places = relationship(
        "Place", backref="cities", cascade="all, delete, delete-orphan"
    )
