import sqlite3


class SqLiteConnector(object):
    """
        Handles the basic connection setup to a sqlite3 database

        Parameters
        ----------
        db_name: str
                The path and the name to /of the database
    """

    def __init__(self, db_name):
        self._db_name = db_name
        self._connection = None  # type: sqlite3.Connection

    def create_db(self):
        """Creates the database if not already existing"""
        self._connection = sqlite3.connect(self._db_name)

    def connect_db(self):
        """Connects to the database or creates if not existing"""
        self._connection = sqlite3.connect(self._db_name)
