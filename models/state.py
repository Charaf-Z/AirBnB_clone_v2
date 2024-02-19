#!/usr/bin/python3
"""State Module for HBNB project."""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """
    State class inherits from BaseModel and Base.

    The State class represents a state in the HBNB project.
    In a database setup, State objects are stored in the 'states' table.

    Attributes:
        id (str): Unique identifier for the State.
        created_at (datetime): The datetime when the State instance
                was created.
        updated_at (datetime): The datetime when the State instance
                was last updated.
        name (str): The name of the State.
        cities (relationship): One-to-many relationship with the City class,
                representing cities associated with the state.
    """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship(
        "City", cascade="all, delete, delete-orphan", backref="state"
    )

    if os.getenv("HBNB_TYPE_STORAGE") != "db":

        @property
        def cities(self):
            """Returns the cities in this State instance."""
            from models import storage

            cities_in_state = []
            for value in list(storage.all(City).values()):
                if value.state_id == self.id:
                    cities_in_state.append(value)
            return cities_in_state
