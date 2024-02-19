#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """
    A base class for all models in the HBNB project.

    Attributes:
        id (str): Unique identifier for the model instance.
        created_at (datetime): The datetime when the model instance
                was created.
        updated_at (datetime): The datetime when the model instance
                was last updated.

    Methods:
        __init__: Initializes a new model instance.
        __str__: Returns a string representation of the model instance.
        save: Updates the 'updated_at' attribute and saves the instance
                to the storage.
        to_dict: Returns a dictionary representation of the model instance.
        delete: Deletes the instance from the storage.
    """

    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DATETIME, nullable=False, default=datetime.utcnow())
    updated_at = Column(DATETIME, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiate a new model instance."""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ("created_at", "updated_at"):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
            if not hasattr(kwargs, "id"):
                setattr(self, "id", str(uuid.uuid4()))
            if not hasattr(kwargs, "created_at"):
                setattr(self, "created_at", datetime.now())
            if not hasattr(kwargs, "updated_at"):
                setattr(self, "updated_at", datetime.now())

    def __str__(self):
        """Return a string representation of the instance."""
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def save(self):
        """Update updated_at with current time when instance is changed."""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format."""
        new_dict = {}
        for key, value in self.__dict__.items():
            if key != "_sa_instance_state":
                if isinstance(value, datetime):
                    new_dict[key] = value.isoformat()
                else:
                    new_dict[key] = value
        new_dict["__class__"] = type(self).__name__
        return new_dict

    def delete(self):
        """Delete the current instance from the storage (models.storage)."""
        from models import storage

        storage.delete(self)
