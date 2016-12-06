CREATE_REPORTS = ('CREATE TABLE Reports '
                  '(id INTEGER NOT NULL,'
                  'current_resolution TEXT,'
                  'current_status TEXT,'
                  'opening INTEGER NOT NULL,'
                  'reporter INTEGER NOT NULL,'
                  ' PRIMARY KEY (id))'
                  )
CREATE_ASSIGNED_TO = ('CREATE TABLE AssignedTo('
                      'id INTEGER NOT NULL,'
                      'what TEXT,'
                      'timestamp INTEGER NOT NULL,'  # do not use when since it is a reserved keyword
                      'who INTEGER NOT NULL,'
                      'FOREIGN KEY (id) REFERENCES Reports(id))'
                      )

CREATE_BUG_STATUS = ('CREATE TABLE BugStatus('
                     'id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES Reports(id))'
                     )

CREATE_CC = ('CREATE TABLE CC('
             'id INTEGER NOT NULL,'
             'what TEXT,'
             'timestamp INTEGER NOT NULL,'
             'who INTEGER NOT NULL,'
             'FOREIGN KEY (id) REFERENCES Reports(id))'
             )

CREATE_COMPONENTS = ('CREATE TABLE Components('
                     'id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES Reports(id))'
                     )

CREATE_OPERATION_SYSTEM = ('CREATE TABLE OperationSystem('
                           'id INTEGER NOT NULL,'
                           'what TEXT,'
                           'timestamp INTEGER NOT NULL,'
                           'who INTEGER NOT NULL,'
                           'FOREIGN KEY (id) REFERENCES Reports(id))'
                           )

CREATE_PRIORITY = ('CREATE TABLE Priority('
                   'id INTEGER NOT NULL,'
                   'what TEXT,'
                   'timestamp INTEGER NOT NULL,'
                   'who INTEGER NOT NULL,'
                   'FOREIGN KEY (id) REFERENCES Reports(id))'
                   )

CREATE_PRODUCT = ('CREATE TABLE Product('
                  'id INTEGER NOT NULL,'
                  'what TEXT,'
                  'timestamp INTEGER NOT NULL,'
                  'who INTEGER NOT NULL,'
                  'FOREIGN KEY (id) REFERENCES Reports(id))'
                  )

CREATE_RESOLUTION = ('CREATE TABLE Resolution('
                     'id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES Reports(id))'
                     )

CREATE_SEVERITY = ('CREATE TABLE Severity('
                     'id INTEGER NOT NULL,'
                     'what TEXT,'
                     'timestamp INTEGER NOT NULL,'
                     'who INTEGER NOT NULL,'
                     'FOREIGN KEY (id) REFERENCES Reports(id))'
                     )

CREATE_SHORT_DESCRIPTION = ('CREATE TABLE ShortDesc('
                            'id INTEGER NOT NULL,'
                            'what TEXT,'
                            'timestamp INTEGER NOT NULL,'
                            'who INTEGER NOT NULL,'
                            'FOREIGN KEY (id) REFERENCES Reports(id))'
                            )

CREATE_VERSION = ('CREATE TABLE Version('
                  'id INTEGER NOT NULL,'
                  'what TEXT,'
                  'timestamp INTEGER NOT NULL,'
                  'who INTEGER NOT NULL,'
                  'FOREIGN KEY (id) REFERENCES Reports(id))'
                  )
