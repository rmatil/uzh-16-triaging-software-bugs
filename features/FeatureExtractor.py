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
