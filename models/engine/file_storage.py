#!/usr/bin/python3
'''
module: models/engine/file_storage
Holds class FileStorage
'''
import json
import models


class FileStorage:
    '''writes to JSON file and reads objects from JSON file.'''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''Return a dictionary of all objects'''
        new_dict = {}
        if cls is None:
            return self.__objects

        if cls != "":
            for key, value in self.__objects.items():
                if cls == key.split(".")[0]:
                    new_dict[key] = value
            return new_dict
        else:
            return self.__objects

    def new(self, obj):
        '''Place in __objects a new object with key <obj class name>.id'''
        k = str(obj.__class__.__name__) + "." + str(obj.id)
        val_dict = obj
        FileStorage.__objects[k] = val_dict

    def save(self):
        '''Save objs to JSON file.'''
        objs_dict = {}
        for key, value in FileStorage.__objects.items():
            objs_dict[key] = value.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objs_dict, fd)

    def reload(self):
        '''Reads instances from JSON file to __objects.'''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as f:
                FileStorage.__objects = json.load(f)
            for key, value in FileStorage.__objects.items():
                cls_name = value["__class__"]
                cls_name = models.classes[cls_name]
                FileStorage.__objects[key] = cls_name(**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''Deletes an object'''
        if obj is not None:
            k = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(k, None)
            self.save()

    def close(self):
        '''Calls the reload method.'''
        self.reload()
