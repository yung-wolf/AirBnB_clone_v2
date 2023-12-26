#!/usr/bin/python3
""" State Module for HBNB project """
import models
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", back_populates="states", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            Getter attribute cities that returns the list of City instances with state_id 
            equals to the current State.id
            """
            l_cities = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    l_cities.append(city)
            return l_cities
