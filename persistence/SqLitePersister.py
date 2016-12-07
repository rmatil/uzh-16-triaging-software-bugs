import csv
import re
import sqlite3

from persistence import sqliteQueries


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
        if self.connection is None:
            raise Exception("Open database connection first")

        self.connection.execute(sqliteQueries.CREATE_ASSIGNED_TO)
        self.connection.execute(sqliteQueries.CREATE_BUG_STATUS)
        self.connection.execute(sqliteQueries.CREATE_CC)
        self.connection.execute(sqliteQueries.CREATE_COMPONENTS)
        self.connection.execute(sqliteQueries.CREATE_OPERATION_SYSTEM)
        self.connection.execute(sqliteQueries.CREATE_PRIORITY)
        self.connection.execute(sqliteQueries.CREATE_PRODUCT)
        self.connection.execute(sqliteQueries.CREATE_REPORTS)
        self.connection.execute(sqliteQueries.CREATE_RESOLUTION)
        self.connection.execute(sqliteQueries.CREATE_SEVERITY)
        self.connection.execute(sqliteQueries.CREATE_SHORT_DESCRIPTION)
        self.connection.execute(sqliteQueries.CREATE_VERSION)

    def import_main_data(self, source, table):
        """
            Import the csv data at the given path into the given table name.
            Note, that this method assumes a table with the columns: id, current_resolution, current_status, opening, reporter

            Parameters
            ----------
            source: str
                    The absolute path to the CSV file which should be imported
            table: str
                    The table name to which the data should be added. Note, that keys and table columns have to match
        """
        if self.connection is None:
            raise Exception("Open database connection first")

        with open(source, 'r') as source_csv_file:
            # assumes a header in the csv file
            dict_reader = csv.DictReader(source_csv_file)
            rows = [(i['id'], i['current_resolution'], i['current_status'], i['opening'], i['reporter']) for i in
                    dict_reader]

        self.connection.executemany(
            "INSERT INTO %s (id, current_resolution, current_status, opening, reporter) VALUES (?, ?, ?, ?, ?);" % table,
            rows)
        self.connection.commit()

    def import_additional_data(self, source, table):
        """
            Import the csv data at the given path into the given table name.
            Note, that this method assumes a table with the columns: id, what, timestamp, who

            Parameters
            ----------
            source: str
                    The absolute path to the CSV file which should be imported
            table: str
                    The table name to which the data should be added. Note, that keys and table columns have to match
        """
        if self.connection is None:
            raise Exception("Open database connection first")

        with open(source, 'r', encoding='utf-8') as source_csv_file:
            content = source_csv_file.read()
            source_csv_file.close()
            # this regex looks for 4-tuples in this bloody text (which is completely insane to be in CSV),
            # amongst multiple lines if required.
            # 4 groups will be captured: id, what, timestamp, who.
            rows = re.findall("([0-9]+),((?:.|(?:\n\t)+)*),([0-9]+),([0-9]+)", content)

        self.connection.executemany(
            "INSERT INTO %s (id, what, timestamp, who) VALUES (?, ?, ?, ?);" % table,
            rows)
        self.connection.commit()
