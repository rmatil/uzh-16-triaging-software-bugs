# 1. success-rate
SUCCESSRATE = ('SELECT success.who, success.count*1.0 / (success.count+ fail.count)'
               'FROM (  SELECT assigned_to.who, count(assigned_to.who) AS count'
               'FROM reports'
               'JOIN assigned_to ON reports.bug_id = assigned_to.bug_id'
               'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR'
               'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR'
               'current_status == "VERIVIED" AND reports.current_resolution == "FIXED" OR'
               'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR'
               'current_status == "CLOSED" AND reports.current_resolution == "FIXED"'
               'GROUP BY assigned_to.who) AS success'
               'JOIN ('
               'SELECT assigned_to.who, count(assigned_to.who) AS count FROM reports'
               'JOIN assigned_to ON reports.bug_id = assigned_to.bug_id'
               'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR'
               'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR'
               'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR'
               'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR'
               'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR'
               'current_status == "VERIFIED" AND reports.current_resolution == "INVALID"'
               'GROUP BY assigned_to.who) AS fail'
               'ON success.who = FAIL.who;'
               )

# 2. reputation-rate

REPUTATIONRATE = ('SELECT reporter, nr_closed, nr_failed, (nr_closed*1.0/(nr_closed+nr_failed)) AS reputationRate'
                  'FROM ('
                  'SELECT reputation.reporter, ifnull(nr_closed, 0) AS nr_closed, ifnull(nr_failed, 0) AS nr_failed'
                  'FROM('
                  'SELECT *'
                  'FROM ('
                  'SELECT reporter, count(reporter) AS nr_closed'
                  'FROM reports'
                  'WHERE current_status== "CLOSED"'
                  'GROUP BY reporter'
                  ') AS closed'
                  'LEFT OUTER JOIN ('
                  'SELECT reporter, count(reporter) AS nr_failed'
                  'FROM reports'
                  'WHERE current_status == "CLOSED" AND current_resolution == "WONTFIX" OR'
                  'current_status == "CLOSED" AND current_resolution == "INVALID"'
                  'GROUP BY reporter) AS failed ON failed.reporter=closed.reporter'
                  'UNION ALL'
                  'SELECT *'
                  'FROM ('
                  'SELECT reporter, count(reporter) AS nr_failed'
                  'FROM reports'
                  'WHERE current_status == "CLOSED" AND current_resolution == "WONTFIX" OR'
                  'current_status == "CLOSED" AND current_resolution == "INVALID"'
                  'GROUP BY reporter) AS failed''
                  'LEFT OUTER JOIN ('
                  'SELECT reporter, count(reporter) AS nr_closed'
                  'FROM reports'
                  'WHERE current_status== "CLOSED"'
                  'GROUP BY reporter''
                  ') AS closed ON failed.reporter=closed.reporter) AS reputation) as repRate;
)


# 5. Number of reopenings per bug
REOPENINGS = ('SELECT bug_status.bug_id, bug_status.timestamp, COUNT(bug_status.id) AS count'
              'FROM bug_status'
              'WHERE bug_status.what = "REOPENED"'
              'GROUP BY bug_id'
              'ORDER BY count DESC;'
              )

# 6. Time during which the bug was open
OPEN_TIME = ('SELECT reports.bug_id, minmax.min, minmax.max, (minmax.max - minmax.min) AS difference FROM ('
             'SELECT'
             'bug_id,'
             'MIN(timestamp) AS min,'
             'MAX(timestamp) AS max'
             'FROM resolution'
             'GROUP BY bug_id'
             'ORDER BY bug_id, timestamp'
             ') AS minmax INNER JOIN reports ON minmax.bug_id = reports.bug_id'
             'WHERE reports.current_status IN ("CLOSED")'
             )

# 7. Software module to which bug was assigned to
SOFTWARE_MODULE = ('SELECT reports.bug_id, components.what FROM components'
                   'INNER JOIN reports ON components.bug_id = reports.bug_id'
                   'WHERE reports.current_status = "CLOSED"'
                   'ORDER BY reports.bug_id'
                   )
