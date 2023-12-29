#!/usr/bin/python3
'''
module: models/base_model
Holds the BaseModel class
'''
import uuid
import models
from os import getenv
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    '''
        Base class for other classes.
    '''
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        '''
            Initialize the class.
        '''
        if (len(kwargs) == 0):
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs.get("created_at"):
                kwargs["created_at"] = datetime.strptime(
                    kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.now()
            if kwargs.get("created_at"):
                kwargs["updated_at"] = datetime.strptime(
                    kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.now()
            for key, value in kwargs.items():
                if "__class__" not in key:
                    setattr(self, key, value)
            if not self.id:
                self.id = str(uuid.uuid4())

    def __str__(self):
        '''Return string representation of BaseModel class.'''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        '''
            Update the updated_at attribute.
        '''
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        '''
            Return dictionary rep of BaseModel.
        '''
        tmp_dct = dict(self.__dict__)
        tmp_dct['__class__'] = self.__class__.__name__
        tmp_dct['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        tmp_dct['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        if hasattr(self, "_sa_instance_state"):
            del tmp_dct["_sa_instance_state"]
        return (tmp_dct)

    def __repr__(self):
        '''Return string representation of BaseModel class.'''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id,self.to_dict()))

    def delete(self):
        '''
            Deletes an object
        '''
        models.storage.delete(self)
