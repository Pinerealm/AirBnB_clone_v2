#!/usr/bin/python3
"""Instantiates a storage object, choosing between DBStorage and FileStorage
"""
import os


storage_type = os.getenv('HBNB_TYPE_STORAGE')
if storage_type == 'db':
    from .engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
