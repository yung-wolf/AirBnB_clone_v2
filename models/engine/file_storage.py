#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects

        bag_dict = {}  # to hold objs of cls
        for key, value in self.__objects.items():
            #print(f"cls: {cls.__name__}")
            if cls.__name__ == key.split(".")[0]:
                #print(f"Class Matched: {key.split('.')[0]}")
                bag_dict[key] = value
        return bag_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        k = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[k] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def delete(self, obj=None):
        """ to delete obj from __objects if it’s inside.
            If obj is equal to None, the method does nothing.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.all():
                del self.all()[key]
                self.save()
