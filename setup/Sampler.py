import math

import numpy as np

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

    def getTrainingData(self):
        return self._getSampledData(self._training_table)

    def getValidationData(self):
        return self._getSampledData(self._validation_table)

    def getTestData(self):
        return self._getSampledData(self._test_table)

    def getTestBugIds(self):
        super().connect_db()
        cursor = self._connection.cursor()

        cursor.execute('SELECT bug_id FROM (SELECT data.bug_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, 1 AS success FROM (SELECT * FROM reports INNER JOIN %s t ON t.bug_id = reports.bug_id INNER JOIN features ON features.bug_id = reports.bug_id) AS data WHERE ( current_status == "RESOLVED" AND data.current_resolution == "WORKSFORME" OR current_status == "RESOLVED" AND data.current_resolution == "FIXED" OR current_status== "VERIFIED" AND data.current_resolution == "FIXED" OR current_status == "CLOSED" AND data.current_resolution == "WORKSFORME" OR current_status == "CLOSED" AND data.current_resolution == "FIXED") UNION SELECT data.bug_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, 0 AS success FROM (SELECT * FROM reports INNER JOIN training_set t ON t.bug_id = reports.bug_id INNER JOIN features ON features.bug_id = reports.bug_id ) AS data WHERE feature_1 NOT NULL AND feature_2 NOT NULL AND feature_3 NOT NULL AND feature_4 NOT NULL AND ( data.current_status == "RESOLVED" AND data.current_resolution == "WONTFIX" OR data.current_status == "RESOLVED" AND data.current_resolution == "INVALID" OR data.current_status == "CLOSED" AND data.current_resolution == "WONTFIX" OR data.current_status == "CLOSED" AND data.current_resolution == "INVALID" OR data.current_status == "VERIFIED" AND data.current_resolution == "WONTFIX" OR data.current_status == "VERIFIED" AND data.current_resolution == "INVALID"))' % self._test_table)

        return cursor.fetchall()

    def _getSampledData(self, table):
        super().connect_db()
        cursor = self._connection.cursor()

        cursor.execute('SELECT feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, success FROM (SELECT data.bug_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, 1 AS success FROM (SELECT * FROM reports INNER JOIN %s t ON t.bug_id = reports.bug_id INNER JOIN features ON features.bug_id = reports.bug_id) AS data WHERE ( current_status == "RESOLVED" AND data.current_resolution == "WORKSFORME" OR current_status == "RESOLVED" AND data.current_resolution == "FIXED" OR current_status== "VERIFIED" AND data.current_resolution == "FIXED" OR current_status == "CLOSED" AND data.current_resolution == "WORKSFORME" OR current_status == "CLOSED" AND data.current_resolution == "FIXED") UNION SELECT data.bug_id, feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, 0 AS success FROM (SELECT * FROM reports INNER JOIN training_set t ON t.bug_id = reports.bug_id INNER JOIN features ON features.bug_id = reports.bug_id ) AS data WHERE feature_1 NOT NULL AND feature_2 NOT NULL AND feature_3 NOT NULL AND feature_4 NOT NULL AND ( data.current_status == "RESOLVED" AND data.current_resolution == "WONTFIX" OR data.current_status == "RESOLVED" AND data.current_resolution == "INVALID" OR data.current_status == "CLOSED" AND data.current_resolution == "WONTFIX" OR data.current_status == "CLOSED" AND data.current_resolution == "INVALID" OR data.current_status == "VERIFIED" AND data.current_resolution == "WONTFIX" OR data.current_status == "VERIFIED" AND data.current_resolution == "INVALID"))' % table)
        X_data_y_data = cursor.fetchall()
        X_data_y_data = np.array(X_data_y_data)

        # split this shit up into features and corresponding labels (i.e. success / failure)
        X_data = X_data_y_data[:, [0, 1, 2, 3, 4, 5, 6, 7, 8]]
        y_data = X_data_y_data[:, [9]]

        return X_data, y_data
