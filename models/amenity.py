#!/usr/bin/python3
"""State Module for HBNB project."""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """
    Amenity class representation.

    The Amenity class inherits from BaseModel and is used to represent
    amenities in the HBNB project. In a database setup,
    Amenity objects are stored in the 'amenities' table.

    Attributes:
        id (str): Unique identifier for the Amenity.
        created_at (datetime): The datetime when the Amenity instance
                was created.
        updated_at (datetime): The datetime when the Amenity instance
                was last updated.
        name (str): The name of the Amenity.
        place_amenities (relationship): Many-to-many relationship
                with the Place class, representing places
                associated with the amenity.
    """

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        place_amenities = relationship("Place", secondary="place_amenity")
