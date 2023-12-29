#!/usr/bin/python3
'''
module: models/engine/db_storage
Holds class DatabaseStorage
'''
import models
from os import getenv
from models.state import State
from models.city import City
from models.base_model import Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    '''Create sql database'''
    __engine = None
    __session = None

    def __init__(self):
        '''Create engine to MySQL databse'''
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        envv = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''Query current database session'''
        db = {}

        if cls != "":
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                k = "{}.{}".format(obj.__class__.__name__, obj.id)
                db[k] = obj
            return db
        else:
            for key, val in models.classes.items():
                if key != "BaseModel":
                    objs = self.__session.query(val).all()
                    if len(objs) > 0:
                        for obj in objs:
                            k = "{}.{}".format(obj.__class__.__name__, obj.id)
                            db_dict[k] = obj
            return db

    def new(self, obj):
        '''Adds object to current db session.'''
        self.__session.add(obj)

    def save(self):
        '''Commit/save all changes of current db session.'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Deletes obj'''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        ''' create all tables in current db session.'''
        self.__session = Base.metadata.create_all(self.__engine)
        fac = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(fac)
        self.__session = Session()

    def close(self):
        '''Remove session'''
        self.__session.close()
