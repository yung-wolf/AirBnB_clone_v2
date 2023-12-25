#!/usr/bin/python3
""" State Module for HBNB project """
import models
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """
            Getter attribute cities that returns the list of City instances with state_id 
            equals to the current State.id
            """
            l_cities = []
            for city in models.storage.all("City").values():
                if city.state_id == self.id:
                    l_cities.append(city)
            return l_cities
