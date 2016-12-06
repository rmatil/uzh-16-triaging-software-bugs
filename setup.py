import os.path as path
from csv_cleaner import CsvCleaner
from persistence import SqLitePersister

source = "resources/eclipse/cc.csv"
target = "resources/eclipse/cc_cleaned.csv"
database = "resources/database/bug_reports.db"

# create absolute paths
source = path.abspath(source)
target = path.abspath(target)
database = path.abspath(database)

# only create the cleaned CC csv if not existing yet
if not path.isfile(target):
    CsvCleaner.clean_cc(source, target)

# create database if not yet existing
persister = SqLitePersister(database)

if not path.isfile(database):
    persister.create_db()
    persister.setup_db_scheme()

