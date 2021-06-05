import logging.config
import sqlite3
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

import mysql.connector



logging.basicConfig(format='%(asctime)s%(name)-12s%(levelname)-8s%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Bookshelf(Base):
    """Create a data model for the database to be set up for capturing book """
    __tablename__ = 'Book_Shelves'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=False, nullable=True)
    #correlation = Column(Float, unique=False, nullable=True)

    def __repr__(self):
        return '<Bookshelf %r>' % self.title


def create_db(engine_string: str) -> None:
    """Create database from provided engine string
    Args:
        engine_string: str - Engine string
    Returns: None
    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Database created.")


def read_table(query, url, user, pwd, db, port, engine_string):
    """
            Function to read a SQL table into Python as a dataframe with the provided query
            Args:
                query = SQL query
            Returns:
                Pandas dataframe
    """
    if user is None and pwd is None:
        conn = sqlite3.connect(engine_string)
    else:
        conn = mysql.connector.connect(host=url, user=user, password=pwd, database=db, port=port)
    df = pd.read_sql(query,conn)

    return df


class BookshelfManager:
    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app: Flask - Flask app
            engine_string: str - Engine string
        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def close(self) -> None:
        """Closes session
        Returns: None
        """
        self.session.close()

    def add_book(self, title: str) -> None:
        """Seeds an existing database with additional Books.
        Args: Title

        Returns:None
        """

        session = self.session
        book = Bookshelf(title=title)
        session.add(book)
        session.commit()
        logger.info("Book name %s is added to database", title)