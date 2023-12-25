#!/usr/bin/python3

"""
module: models/engine/db_storage

Database storage
"""

from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import Base
from models.city import City
from models.state import State


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
        data_dic = {}

        if cls == None:
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                k = f"{obj.__class__.__name__,}.{obj.id}"
                data_dic[k] = obj
            return data_dic
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(v).all()
                    if len(objs) >= 1:
                        for obj in objs:
                            k = f"{obj.__class__.__name__}.{obj.id}"
                            data_dic[k] = obj
            return data_dic

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
        self.__session = Base.metadata.create_all(self.__engine)
        fac = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(fac)
        self.__session = Session()

    def close(self):
        """Delete session attr."""
        self.__session.close()
