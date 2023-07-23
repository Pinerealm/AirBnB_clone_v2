#!/usr/bin/python3
"""The DBStorage module
"""
from ..base_model import Base
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Defines the DBStorage class
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes an instance of the DBStorage class
        """
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER, HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST, HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage

        Args:
            cls (class): The class to filter for
        """
        from ..amenity import Amenity
        from ..city import City
        from ..place import Place
        from ..review import Review
        from ..state import State
        from ..user import User

        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            objs = self.__session.query(cls).all()

        return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                for obj in objs}

    def new(self, obj):
        """Adds a new object to the current database session

        Args:
            obj: The object to add
        """
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session

        Args:
            obj: The object to delete
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and creates the current
        database session
        """
        from ..amenity import Amenity
        from ..base_model import Base
        from ..city import City
        from ..place import Place
        from ..review import Review
        from ..state import State
        from ..user import User

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Closes the current database session
        """
        self.__session.remove()
