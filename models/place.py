#!/usr/bin/python3
"""Place Module for HBNB project."""
import os
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity


if os.getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            nullable=False,
            primary_key=True,
        ),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            nullable=False,
            primary_key=True,
        ),
    )

"""
Represents the many to many relationship table
between Place and Amenity records.
"""


class Place(BaseModel, Base):
    """
    A place to stay.

    The Place class inherits from BaseModel and is used to represent places
    to stay in the HBNB project. In a database setup,
    Place objects are stored in the 'places' table.

    Attributes:
        id (str): Unique identifier for the Place.
        created_at (datetime): The datetime when the Place instance
                was created.
        updated_at (datetime): The datetime when the Place instance
                was last updated.
        city_id (str): The foreign key linking the Place to a City.
        user_id (str): The foreign key linking the Place to a User.
        name (str): The name of the Place.
        description (str): A description of the Place.
        number_rooms (int): The number of rooms in the Place.
        number_bathrooms (int): The number of bathrooms in the Place.
        max_guest (int): The maximum number of guests the Place
                can accommodate.
        price_by_night (int): The price per night for the Place.
        latitude (float): The latitude coordinate of the Place.
        longitude (float): The longitude coordinate of the Place.
        amenity_ids (list): A list of amenity IDs associated
                with the Place (file-based storage only).
        reviews (relationship): One-to-many relationship with the Review class,
                representing reviews associated with the place.
        amenities (relationship): Many-to-many relationship
                with the Amenity class, representing amenities
                associated with the place.
    """

    __tablename__ = "places"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship(
        "Review", cascade="all, delete, delete-orphan", backref="place"
    )
    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        viewonly=False,
        backref="place_amenities",
    )

    if os.getenv("HBNB_TYPE_STORAGE", None) == "db":

        @property
        def amenities(self):
            """Returns the amenities of this Place."""
            from models import storage

            amenities_of_place = []
            for value in storage.all(Amenity).values():
                if value.id in self.amenity_ids:
                    amenities_of_place.append(value)
            return amenities_of_place

        @amenities.setter
        def amenities(self, value):
            """Add an amenity to this Place."""
            if type(value) is Amenity:
                if value.id not in self.amenity_ids:
                    self.amenity_ids.append(value.id)

        @property
        def reviews(self):
            """Returns the reviews of this Place."""
            from models import storage

            reviews_of_place = []
            for value in storage.all(Review).values():
                if value.place_id == self.id:
                    reviews_of_place.append(value)
            return reviews_of_place
