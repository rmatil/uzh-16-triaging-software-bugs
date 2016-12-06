import os.path as path
from csv_cleaner import CsvCleaner

source = "resources/eclipse/cc.csv"
target = "resources/eclipse/cc_cleaned.csv"

# only create the cleaned CC csv if not existing yet
if not path.isfile(target):
    CsvCleaner.clean_cc(source, target)
