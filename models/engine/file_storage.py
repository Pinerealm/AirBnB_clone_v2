#!/usr/bin/python3
"""The FileStorage module
"""
import json


class FileStorage:
    """Serializes instances to a JSON file and deserializes from a JSON file
    to instances

    Attributes:
        __file_path (str): The path to the JSON file
        __objects (dict): A dictionary to store instantiated objects
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage

        Args:
            cls (class): The class to filter for
        """
        temp = {}
        if cls is not None:
            for key, val in self.__objects.items():
                if val.__class__ == cls:
                    temp[key] = val
            return temp
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary

        Args:
            obj: The object to add to storage
        """
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file
        """
        temp = {}
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            temp.update(self.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads file into storage dictionary
        """
        from ..amenity import Amenity
        from ..base_model import BaseModel
        from ..city import City
        from ..place import Place
        from ..review import Review
        from ..state import State
        from ..user import User

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
        except (FileNotFoundError, ValueError):
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

    def close(self):
        """Deserialize JSON file to objects
        """
        self.reload()
