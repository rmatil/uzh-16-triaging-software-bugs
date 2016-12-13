import math

import numpy

from setup import SqLiteConnector
from setup import sqliteQueries


class DbSampler(SqLiteConnector.SqLiteConnector):
    """
        Samples the given data into training, validation and testing sets.

        Parameters
        ----------
        db_name: str
                The database path and name
        training_table: str
                The name of the table in which the bug ids are stored used for training
        validation_table: str
                The name of the table in which the bug ids are stored used for validation
        test_table: str
                The name of the table in which the bug ids are stored used for testing
    """
    def __init__(self, db_name, training_table, validation_table, test_table):
        super().__init__(db_name)
        self._training_table = training_table
        self._validation_table = validation_table
        self._test_table = test_table

    def sample(self):
        """Samples the data into training, validation and test set"""
        super().connect_db()

        cursor = self._connection.cursor()
        # Find all bugs which have all features (1-10)
        cursor.execute(sqliteQueries.FIND_SAMPLE_BUGS)
        rows = cursor.fetchall()

        if len(rows) == 0:
            raise Exception('Cannot sample on zero found bugs')

        print('[DbSampler] Found %s bugs to split into training, validation and test data' % len(rows))

        no_of_rows = len(rows)
        half = int(math.floor(no_of_rows / 2))  # 50%
        quarter = int(math.floor(half / 2))  # 25%

        numpy.random.shuffle(rows)

        training_sample, validation_sample, test_sample = rows[:half], rows[half:half + quarter], rows[half + quarter:]

        print('[DbSampler] Got %s training, %s validation and %s test bugs' % (len(training_sample), len(validation_sample), len(test_sample)))

        print('[DbSampler] Dropping all previously sampled training data')
        cursor.execute('DELETE FROM %s' % self._training_table)
        print('[DbSampler] Dropping all previously sampled validation data')
        cursor.execute('DELETE FROM %s' % self._validation_table)
        print('[DbSampler] Dropping all previously sampled test data')
        cursor.execute('DELETE FROM %s' % self._test_table)

        print('[DbSampler] Inserting sampled data...')

        self._connection.executemany(
            "INSERT INTO %s (bug_id) VALUES (?);" % self._training_table, training_sample)
        self._connection.executemany(
            "INSERT INTO %s (bug_id) VALUES (?);" % self._validation_table, validation_sample)
        self._connection.executemany(
            "INSERT INTO %s (bug_id) VALUES (?);" % self._test_table, test_sample)
        self._connection.commit()

        print('[DbSampler] Done.')
