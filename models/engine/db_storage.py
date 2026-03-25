#!/usr/bin/python3
"""The DBStorage module
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import storage_type

if storage_type == 'db':
    from ..base_model import Base
else:
    print("DBStorage will not work without a database storage type set.")
    os._exit(1)


class DBStorage:
    """Defines the DBStorage class

    Attributes:
        __engine (sqlalchemy.engine.Engine): The working SQLAlchemy engine
        __session (sqlalchemy.orm.session.Session): The working SQLAlchemy
                                                    session
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

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER, HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST, HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)  # type: ignore

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
            objs = self.__session.query(State).all()  # type: ignore
            objs.extend(self.__session.query(City).all())  # type: ignore
            objs.extend(self.__session.query(User).all())  # type: ignore
            objs.extend(self.__session.query(Place).all())  # type: ignore
            objs.extend(self.__session.query(Review).all())  # type: ignore
            objs.extend(self.__session.query(Amenity).all())  # type: ignore
        else:
            objs = self.__session.query(cls).all()  # type: ignore

        return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                for obj in objs}

    def new(self, obj):
        """Adds a new object to the current database session

        Args:
            obj: The object to add
        """
        self.__session.add(obj)  # type: ignore

    def save(self):
        """Commits all changes in the current database session
        """
        self.__session.commit()  # type: ignore

    def delete(self, obj=None):
        """Deletes an object from the current database session

        Args:
            obj: The object to delete
        """
        if obj is not None:
            self.__session.delete(obj)  # type: ignore

    def reload(self):
        """Creates all tables in the database and creates the current
        database session
        """
        from ..amenity import Amenity
        from ..city import City
        from ..place import Place
        from ..review import Review
        from ..state import State
        from ..user import User

        Base.metadata.create_all(self.__engine)  # type: ignore
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Closes the current database session
        """
        self.__session.remove()  # type: ignore
