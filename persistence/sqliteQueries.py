CREATE_REPORTS = ('CREATE TABLE reports '
                  '(id INTEGER NOT NULL,'
                  'current_resolution TEXT,'
                  'current_status TEXT,'
                  'opening INTEGER NOT NULL,'
                  'reporter INTEGER NOT NULL,'
                  ' PRIMARY KEY (id))'
                  )
CREATE_ASSIGNED_TO = ('CREATE TABLE assigned_to('
                      'id INTEGER NOT NULL,'
                      'what TEXT,'
                      'timestamp INTEGER NOT NULL,'  # do not use when since it is a reserved keyword
                      'who INTEGER NOT NULL,'
                      'FOREIGN KEY (id) REFERENCES reports(id))'
                      )

CREATE_BUG_STATUS = ('CREATE TABLE bug_status('
                     'id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES reports(id))'
                     )

CREATE_CC = ('CREATE TABLE cc('
             'id INTEGER NOT NULL,'
             'what TEXT,'
             'timestamp INTEGER NOT NULL,'
             'who INTEGER NOT NULL,'
             'FOREIGN KEY (id) REFERENCES reports(id))'
             )

CREATE_COMPONENTS = ('CREATE TABLE components('
                     'id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES reports(id))'
                     )

CREATE_OPERATION_SYSTEM = ('CREATE TABLE operation_system('
                           'id INTEGER NOT NULL,'
                           'what TEXT,'
                           'timestamp INTEGER NOT NULL,'
                           'who INTEGER NOT NULL,'
                           'FOREIGN KEY (id) REFERENCES reports(id))'
                           )

CREATE_PRIORITY = ('CREATE TABLE priority('
                   'id INTEGER NOT NULL,'
                   'what TEXT,'
                   'timestamp INTEGER NOT NULL,'
                   'who INTEGER NOT NULL,'
                   'FOREIGN KEY (id) REFERENCES reports(id))'
                   )

CREATE_PRODUCT = ('CREATE TABLE product('
                  'id INTEGER NOT NULL,'
                  'what TEXT,'
                  'timestamp INTEGER NOT NULL,'
                  'who INTEGER NOT NULL,'
                  'FOREIGN KEY (id) REFERENCES reports(id))'
                  )

CREATE_RESOLUTION = ('CREATE TABLE resolution('
                     'id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES reports(id))'
                     )

CREATE_SEVERITY = ('CREATE TABLE severity('
                     'id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES reports(id))'
                     )

CREATE_SHORT_DESCRIPTION = ('CREATE TABLE short_desc('
                            'id INTEGER NOT NULL,'
                            'what TEXT,'
                            'timestamp INTEGER NOT NULL,'
                            'who INTEGER NOT NULL,'
                            'FOREIGN KEY (id) REFERENCES reports(id))'
                            )

CREATE_VERSION = ('CREATE TABLE version('
                  'id INTEGER NOT NULL,'
                  'what TEXT,'
                  'timestamp INTEGER NOT NULL,'
                  'who INTEGER NOT NULL,'
                  'FOREIGN KEY (id) REFERENCES reports(id))'
                  )
