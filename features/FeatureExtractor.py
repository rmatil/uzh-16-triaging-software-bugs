
# Number of reopenings per bug
REOPENINGS = ('SELECT bug_status.bug_id, bug_status.timestamp, COUNT(bug_status.id) AS count'
              'FROM bug_status'
              'WHERE bug_status.what = "REOPENED"'
              'GROUP BY bug_id'
              'ORDER BY count DESC'
              )
