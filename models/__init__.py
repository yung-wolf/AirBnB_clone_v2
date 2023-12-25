#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
from models.base_model import BaseModel
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.user import User
from models.review import Review
from models.place import Place

classes = {"User": User, "Place": Place, "State": State, "City": City,
           "Review": Review, "BaseModel": BaseModel, "Amenity": Amenity}

if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
    from models.engine import db_storage
    storage = db_storage.DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
