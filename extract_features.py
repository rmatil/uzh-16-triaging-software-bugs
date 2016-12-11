import os.path as path

from features import FeatureImporter

database = "resources/database/bug_reports.db"
database = path.abspath(database)

feature_table = 'features'

if not path.isfile(database):
    raise Exception("Run setup.py before trying to extract features")

feature_importer = FeatureImporter.FeatureImporter(database)

feature_importer.connect_db()
feature_importer.generate_empty_entries(feature_table)
feature_importer.generate_and_import_feature_1(feature_table)
feature_importer.generate_and_import_feature_2(feature_table)
