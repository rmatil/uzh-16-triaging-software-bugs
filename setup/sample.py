import os.path as path

from setup import Sampler

# Sample data based on the current feature database
# Make sure, you have ran setup.py first

database = "../resources/database/bug_reports.db"
database = path.abspath(database)

sampler = Sampler.DbSampler(database, 'training_set', 'validation_set', 'test_set')
sampler.sample()
