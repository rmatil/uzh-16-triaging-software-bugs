CREATE_REPORTS = ('CREATE TABLE reports '
                  '(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                  'bug_id INTEGER NOT NULL,'
                  'current_resolution TEXT,'
                  'current_status TEXT,'
                  'opening INTEGER NOT NULL,'
                  'reporter INTEGER NOT NULL)'
                  )

CREATE_ASSIGNED_TO = ('CREATE TABLE assigned_to('
                      'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                      'bug_id INTEGER NOT NULL,'
                      'what TEXT,'
                      'timestamp INTEGER NOT NULL,'  # do not use when since it is a reserved keyword
                      'who INTEGER NOT NULL,'
                      'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                      )

CREATE_BUG_STATUS = ('CREATE TABLE bug_status('
                     'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                     'bug_id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                     )

CREATE_CC = ('CREATE TABLE cc('
             'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
             'bug_id INTEGER NOT NULL,'
             'what TEXT,'
             'timestamp INTEGER NOT NULL,'
             'who INTEGER NOT NULL,'
             'FOREIGN KEY (id) REFERENCES reports(bug_id))'
             )

CREATE_COMPONENTS = ('CREATE TABLE components('
                     'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                     'bug_id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                     )

CREATE_OPERATION_SYSTEM = ('CREATE TABLE operation_system('
                           'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                           'bug_id INTEGER NOT NULL,'
                           'what TEXT,'
                           'timestamp INTEGER NOT NULL,'
                           'who INTEGER NOT NULL,'
                           'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                           )

CREATE_PRIORITY = ('CREATE TABLE priority('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                   'bug_id INTEGER NOT NULL,'
                   'what TEXT,'
                   'timestamp INTEGER NOT NULL,'
                   'who INTEGER NOT NULL,'
                   'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                   )

CREATE_PRODUCT = ('CREATE TABLE product('
                  'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                  'bug_id INTEGER NOT NULL,'
                  'what TEXT,'
                  'timestamp INTEGER NOT NULL,'
                  'who INTEGER NOT NULL,'
                  'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                  )

CREATE_RESOLUTION = ('CREATE TABLE resolution('
                     'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                     'bug_id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                     )

CREATE_SEVERITY = ('CREATE TABLE severity('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                   'bug_id INTEGER NOT NULL,'
                   'what TEXT,'
                   'timestamp INTEGER NOT NULL,'
                   'who INTEGER NOT NULL,'
                   'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                   )

CREATE_SHORT_DESCRIPTION = ('CREATE TABLE short_desc('
                            'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                            'bug_id INTEGER NOT NULL,'
                            'what TEXT,'
                            'timestamp INTEGER NOT NULL,'
                            'who INTEGER NOT NULL,'
                            'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                            )

CREATE_VERSION = ('CREATE TABLE version('
                  'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                  'bug_id INTEGER NOT NULL,'
                  'what TEXT,'
                  'timestamp INTEGER NOT NULL,'
                  'who INTEGER NOT NULL,'
                  'FOREIGN KEY (id) REFERENCES reports(bug_id))'
                  )

CREATE_TRAINING_SET = ('CREATE TABLE training_set('
                       'bug_id INTEGER PRIMARY KEY NOT NULL,'
                       'FOREIGN KEY (bug_id) REFERENCES reports(bug_id))'
                       )

CREATE_VALIDATION_SET = ('CREATE TABLE validation_set('
                         'bug_id INTEGER PRIMARY KEY NOT NULL,'
                         'FOREIGN KEY (bug_id) REFERENCES reports(bug_id))'
                         )

CREATE_TEST_SET = ('CREATE TABLE test_set('
                   'bug_id INTEGER PRIMARY KEY NOT NULL,'
                   'FOREIGN KEY (bug_id) REFERENCES reports(bug_id))'
                   )

CREATE_FEATURES = ('CREATE TABLE features('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                   'bug_id INTEGER NOT NULL,'
                   'feature_1 REAL,'
                   'feature_2 REAL,'
                   'feature_3 REAL,'
                   'feature_4 REAL,'
                   'feature_5 REAL,'
                   'feature_6 REAL,'
                   'feature_7 REAL,'
                   'feature_8 REAL,'
                   'feature_9 REAL,'
                   'feature_10 REAL,'
                   'FOREIGN KEY (bug_id) REFERENCES reports(bug_id))'
                   )
