from setup import SqLiteConnector
from features import featureQueries


class FeatureImporter(SqLiteConnector.SqLiteConnector):
    """
        Generates and imports feature data for each bug

        Parameters
        ----------
        db_name: str
                The path and the name to / of the database
    """

    def __init__(self, db_name):
        super().__init__(db_name)

    def generate_empty_entries(self, table):
        """Insert empty rows for all bugs"""
        rows = self._fetch_many("SELECT DISTINCT bug_id FROM reports ORDER BY bug_id")
        self._insert_many("INSERT INTO %s (bug_id) VALUES (?)" % table, rows)

    def generate_and_import_feature_1(self, table):
        """Calculate and insert feature 1: Success Rate of Bug Assignee"""
        rows = self._fetch_many(featureQueries.SUCCESS_RATE)
        self._insert_many('UPDATE %s SET feature_1 = ? WHERE bug_id = ?' % table, rows)

    def generate_and_import_feature_2(self, table):
        """Calculate and insert feature 2: Reputation of Bug Reporter"""
        rows = self._fetch_many(featureQueries.REPUTATION_RATE)
        self._insert_many('UPDATE %s SET feature_2 = ? WHERE bug_id = ?' % table, rows)

    def generate_and_import_feature_3(self, table):
        """Calculate and insert feature 3: Ratio of Success of a bug report for every reporter-assignee pair"""
        rows = self._fetch_many(featureQueries.REPORTER_ASSIGNEE_RATE)
        self._insert_many('UPDATE %s SET feature_3 = ? WHERE bug_id = ?' % table, rows)

    def generate_and_import_feature_4(self, table):
        """Calculate and insert feature 4: Impact of reassignments of a bug"""
        rows = self._fetch_many(featureQueries.REASSINGMENTS)
        self._insert_many('UPDATE %s SET feature_4 = ? WHERE bug_id = ?' % table, rows)

    def generate_and_import_feature_5(self, table):
        """Calculate and insert feature 5: Number of reponenings of a bug"""
        rows = self._fetch_many(featureQueries.REOPENINGS)
        self._insert_many('UPDATE %s SET feature_5 = ? WHERE bug_id = ?' % table, rows)

    def generate_and_import_feature_6(self, table):
        """Calculate and insert feature 6: Time during which the bug was open"""
        rows = self._fetch_many(featureQueries.OPEN_TIME)
        self._insert_many('UPDATE %s SET feature_6 = ? WHERE bug_id = ?' % table, rows)

    def generate_and_import_feature_7(self, table):
        """Calculate and insert feature 7: Software module to which bug was assigned to"""
        rows = self._fetch_many(featureQueries.SOFTWARE_MODULE)
        self._insert_many('UPDATE %s SET feature_7 = ? WHERE bug_id = ?' % table, rows)

    def generate_and_import_feature_8(self, table):
        """Calculate and insert feature 8: Relationship between reporter and Users in CC"""
        rows = self._fetch_many(featureQueries.RELATIONSHIP)
        self._insert_many('UPDATE %s SET feature_8 = ? WHERE bug_id = ?' % table, rows)

    def generate_and_import_feature_9(self, table):
        """Calculate and insert feature 9: Relation of Software Version and Bug Fix"""
        rows = self._fetch_many(featureQueries.SOFTWARE_VERSION)
        self._insert_many('UPDATE %s SET feature_9 = ? WHERE bug_id = ?' % table, rows)

    def generate_and_import_feature_10(self, table):
        """Calculate and insert feature 10: Influence of a bug relation to user interface environment and network"""
        rows = self._fetch_many(featureQueries.BUGNATURE)
        self._insert_many('UPDATE %s SET feature_10 = ? WHERE bug_id = ?' % table, rows)

    def _fetch_many(self, query):
        """Fetches all rows of the given query"""
        if self._connection is None:
            raise Exception("Open database connection first")

        cursor = self._connection.cursor()
        print("[Extracting Feature Data]: %s" % query)
        cursor.execute(query)

        return cursor.fetchall()

    def _insert_many(self, query, data):
        """Inserts the data using the given query"""
        if self._connection is None:
            raise Exception("Open database connection first")

        print("[Inserting Feature Data]: %s" % query)
        self._connection.executemany(query, data)
        self._connection.commit()
