#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage

        Args:
            cls (str): The name of the class to filter for
        """
        temp = {}
        if cls is not None:
            for key, val in self.__objects.items():
                if val.__class__ == cls:
                    temp[key] = val
            return temp
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary

        Args:
            obj: The object to add to storage
        """
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        with open(self.__file_path, 'w') as f:
            temp.update(self.__objects)
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
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if present

        Args:
            obj: The object to delete
        """
        if obj is None:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in self.all():
            del self.all()[key]
            self.save()
