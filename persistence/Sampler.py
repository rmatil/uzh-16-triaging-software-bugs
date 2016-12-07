import sqlite3
import math
import numpy


class Sampler(object):
    def __init__(self, db, source_table, training_table, validation_table, test_table):
        self.db = db
        self.source_table = source_table
        self.training_table = training_table
        self.validation_table = validation_table
        self.test_table = test_table

    def sample(self):
        connection = sqlite3.connect(self.db)

        cursor = connection.cursor()
        cursor.execute('SELECT bug_id FROM %s' % self.source_table)
        rows = cursor.fetchall()

        noOfRows = len(rows)
        half = int(math.floor(noOfRows / 2))  # 50%
        quarter = int(math.floor(half / 2))  # 25%

        numpy.random.shuffle(rows)

        training_sample, validation_sample, test_sample = rows[:half], rows[half:half + quarter], rows[half + quarter:]

        connection.executemany(
            "INSERT INTO %s (bug_id) VALUES (?);" % self.training_table,
            training_sample)
        connection.executemany(
            "INSERT INTO %s (bug_id) VALUES (?);" % self.validation_table,
            validation_sample)
        connection.executemany(
            "INSERT INTO %s (bug_id) VALUES (?);" % self.test_table,
            test_sample)
        connection.commit()
