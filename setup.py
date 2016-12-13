import os.path as path

from setup import Cleaner
from setup import SqLitePersister

cc_source = "resources/eclipse/cc.csv"
cc_target = "resources/eclipse/cc_cleaned.csv"
database = "resources/database/bug_reports.db"

# create absolute paths
cc_source = path.abspath(cc_source)
cc_target = path.abspath(cc_target)
database = path.abspath(database)

# only create the cleaned CC csv if not existing yet
if not path.isfile(cc_target):
    print("Cleaning cc.csv... ")
    Cleaner.CsvCleaner.clean_cc(cc_source, cc_target)
    print("Done \n")

# create database if not yet existing
persister = SqLitePersister.SqLitePersister(database)

if not path.isfile(database):
    print("Creating database at %s... " % database)
    persister.create_db()
    print("Done. \n")
    print("Setting up DB schema... ")
    persister.setup_db_scheme()
    print("Done. \n")

    # persist this bloody csv data
    print("Importing data... ")
    persister.import_main_data(path.abspath("resources/eclipse/reports.csv"), 'reports')
    persister.import_additional_data(path.abspath("resources/eclipse/assigned_to.csv"), "assigned_to")
    persister.import_additional_data(path.abspath("resources/eclipse/bug_status.csv"), "bug_status")
    persister.import_additional_data(path.abspath("resources/eclipse/cc_cleaned.csv"), "cc")
    persister.import_additional_data(path.abspath("resources/eclipse/component.csv"), "components")
    persister.import_additional_data(path.abspath("resources/eclipse/op_sys.csv"), "operation_system")
    persister.import_additional_data(path.abspath("resources/eclipse/priority.csv"), "priority")
    persister.import_additional_data(path.abspath("resources/eclipse/product.csv"), "product")
    persister.import_additional_data(path.abspath("resources/eclipse/resolution.csv"), "resolution")
    persister.import_additional_data(path.abspath("resources/eclipse/severity.csv"), "severity")
    persister.import_additional_data(path.abspath("resources/eclipse/short_desc.csv"), "short_desc")
    persister.import_additional_data(path.abspath("resources/eclipse/version.csv"), "version")
    print("Done. \n")
else:
    print("Connecting to database at %s... " % database)
    persister.connect_db()
    print("Done. \n")
