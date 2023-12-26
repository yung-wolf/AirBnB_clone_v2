#!/usr/bin/python3

"""
module: models/engine/db_storage

Database storage
"""

import models
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


class DBStorage:
    """Create SQL DB storage using sqlalchemy."""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the class. Create and link engind to mysql db."""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        envt = getenv("HBNB_ENV", "none")
        self.__engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}/{database}", pool_pre_ping=True)
        if envt == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        if cls is None:
            objects = self.__session.query(User).all()
            objects.extend(self.__session.query(State).all())
            objects.extend(self.__session.query(City).all())
            objects.extend(self.__session.query(Place).all())
            objects.extend(self.__session.query(Review).all())
            objects.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objects = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """ Add obj to current db session"""
        self.__session.add(obj)

    def save(self):
        """Save all modifications to current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from current db session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload session"""
        Base.metadata.create_all(self.__engine)
        fac = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(fac)
        self.__session = Session()

    def close(self):
        """Delete session attr."""
        self.__session.close()
