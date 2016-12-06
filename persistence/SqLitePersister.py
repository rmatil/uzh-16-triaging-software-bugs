import sqlite3
import sqliteQueries


class SqLitePersister(object):
    """
        Handles common functionalities in order to setup the
        database for later working on the dataset

        Parameters
        ----------
        db_name: str
                The path and the name to /of the database
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None  # type: sqlite3.Connection

    def create_db(self):
        """Creates the database if not already existing"""
        self.connection = sqlite3.connect(self.db_name)

    def setup_db_scheme(self):
        """Creates the database schema"""
        self.connection.execute(sqliteQueries.CREATE_ASSIGNED_TO)
        self.connection.execute(sqliteQueries.CREATE_BUG_STATUS)
        self.connection.execute(sqliteQueries.CREATE_CC)
        self.connection.execute(sqliteQueries.CREATE_COMPONENTS)
        self.connection.execute(sqliteQueries.CREATE_OPERATION_SYSTEM)
        self.connection.execute(sqliteQueries.CREATE_PRIORITY)
        self.connection.execute(sqliteQueries.CREATE_PRODUCT)
        self.connection.execute(sqliteQueries.CREATE_REPORTS)
        self.connection.execute(sqliteQueries.CREATE_RESOLUTION)
        self.connection.execute(sqliteQueries.CREATE_OPERATION_SYSTEM)
        self.connection.execute(sqliteQueries.CREATE_SHORT_DESCRIPTION)
        self.connection.execute(sqliteQueries.CREATE_VERSION)
