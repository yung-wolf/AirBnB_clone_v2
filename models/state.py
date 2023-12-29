#!/usr/bin/python3
'''
module: models/state
Holds the State class
'''
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models


class State(BaseModel, Base):
    '''
        Models a State in the US.
        Draw relationship between class State (parent) to City (child)
    '''
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            '''
                Return list of city instances
            '''
            l_cities = []
            for city in models.storage.all("City").values():
                if city.state_id == self.id:
                    l_cities.append(city)
            return l_cities
