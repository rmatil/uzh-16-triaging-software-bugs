# 1. success-rate
SUCCESS_RATE = ('SELECT '
                'success_count * 1.0 / (success_count + failed_count) AS success_rate, '
                'reports.bug_id '
                'FROM ( '
                'SELECT '
                'success.who                      AS who, '
                'ifnull(success.success_count, 0) AS success_count, '
                'ifnull(failed.fail_count, 0)     AS failed_count '
                'FROM ( '
                'SELECT '
                'assigned_to.who, '
                'count(assigned_to.who) AS success_count '
                'FROM reports '
                'INNER JOIN assigned_to ON reports.bug_id = assigned_to.bug_id '
                'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR '
                'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "FIXED" '
                'GROUP BY assigned_to.who '
                ') AS success '
                'LEFT OUTER JOIN ( '
                'SELECT '
                'assigned_to.who, '
                'count(assigned_to.who) AS fail_count '
                'FROM reports '
                'INNER JOIN assigned_to ON reports.bug_id = assigned_to.bug_id '
                'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "INVALID" '
                'GROUP BY assigned_to.who '
                ') AS failed '
                'ON success.who = failed.who '
                'UNION '
                'SELECT '
                'failed.who                       AS who, '
                'ifnull(success.success_count, 0) AS success_count, '
                'ifnull(failed.fail_count, 0)     AS failed_count '
                'FROM ( '
                'SELECT '
                'assigned_to.who, '
                'count(assigned_to.who) AS fail_count '
                'FROM reports '
                'INNER JOIN assigned_to ON reports.bug_id = assigned_to.bug_id '
                'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "INVALID" '
                'GROUP BY assigned_to.who '
                ') AS failed '
                'LEFT OUTER JOIN ( '
                'SELECT '
                'assigned_to.who, '
                'count(assigned_to.who) AS success_count '
                'FROM reports '
                'INNER JOIN assigned_to ON reports.bug_id = assigned_to.bug_id '
                'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR '
                'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "FIXED" '
                'GROUP BY assigned_to.who '
                ') AS success '
                'ON success.who = failed.who '
                ') INNER JOIN reports ON reports.reporter = who '
                'ORDER BY reports.bug_id;')

# 2. reputation-rate

REPUTATION_RATE = (
    'SELECT '
    '(nr_closed * 1.0 / (nr_closed + nr_failed)) AS reputationRate, '
    'reports.bug_id '
    'FROM ( '
    'SELECT '
    'reputation.reporter, '
    'ifnull(nr_closed, 0) AS nr_closed, '
    'ifnull(nr_failed, 0) AS nr_failed '
    'FROM ( '
    'SELECT '
    'closed.reporter, '
    'closed.nr_closed, '
    'failed.reporter, '
    'failed.nr_failed '
    'FROM ( '
    'SELECT '
    'reporter, '
    'count(reporter) AS nr_closed '
    'FROM reports '
    'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR '
    'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR '
    'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR '
    'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR '
    'current_status == "CLOSED" AND reports.current_resolution == "FIXED" '
    'GROUP BY reporter '
    ') AS closed '
    'LEFT OUTER JOIN ( '
    'SELECT '
    'reporter, '
    'count(reporter) AS nr_failed '
    'FROM reports '
    'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR '
    'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR '
    'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR '
    'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR '
    'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR '
    'current_status == "VERIFIED" AND reports.current_resolution == "INVALID" '
    'GROUP BY reporter) '
    'AS failed '
    'ON failed.reporter = closed.reporter '
    'UNION '
    'SELECT '
    'closed.reporter, '
    'closed.nr_closed, '
    'failed.reporter, '
    'failed.nr_failed '
    'FROM ( '
    'SELECT '
    'reporter, '
    'count(reporter) AS nr_failed '
    'FROM reports '
    'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR '
    'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR '
    'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR '
    'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR '
    'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR '
    'current_status == "VERIFIED" AND reports.current_resolution == "INVALID" '
    'GROUP BY reporter '
    ') AS failed '
    'LEFT OUTER JOIN ( '
    'SELECT '
    'reporter, '
    'count(reporter) AS nr_closed '
    'FROM reports '
    'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR '
    'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR '
    'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR '
    'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR '
    'current_status == "CLOSED" AND reports.current_resolution == "FIXED" '
    'GROUP BY reporter '
    ') AS closed '
    'ON failed.reporter = closed.reporter '
    ') AS reputation '
    ') AS repRate '
    'INNER JOIN reports ON reports.reporter = repRate.reporter '
    'ORDER BY reports.bug_id'
)

# 3. ratio between success and reporter-assignee pair
# ratio of success of a bug report for every reporter-assignee pair

REPORTER_ASSIGNEE_RATE = ('SELECT '
                          '(nr_closed * 1.0 / (nr_closed + nr_failed)) AS reputationRate, '
                          'reports.bug_id '
                          'FROM ( '
                          'SELECT '
                          'repRate.who, '
                          'ifnull(success_count, 0) AS nr_closed, '
                          'ifnull(failed_count, 0)  AS nr_failed '
                          'FROM ( '
                          'SELECT '
                          'success.who, '
                          'success.success_count, '
                          'failed.failed_count '
                          'FROM ( '
                          'SELECT '
                          'assigned_to.who, '
                          'count(assigned_to.who) AS success_count '
                          'FROM reports '
                          'JOIN assigned_to ON reports.bug_id = assigned_to.bug_id '
                          'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR '
                          'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR '
                          'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR '
                          'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR '
                          'current_status == "CLOSED" AND reports.current_resolution == "FIXED" '
                          'GROUP BY assigned_to.who '
                          ') AS success '
                          'LEFT OUTER JOIN ( '
                          'SELECT '
                          'assigned_to.who, '
                          'count(assigned_to.who) AS failed_count '
                          'FROM reports '
                          'JOIN assigned_to ON reports.bug_id = assigned_to.bug_id '
                          'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR '
                          'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR '
                          'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR '
                          'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR '
                          'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR '
                          'current_status == "VERIFIED" AND reports.current_resolution == "INVALID" '
                          'GROUP BY assigned_to.who) AS failed '
                          'ON success.who = failed.who '
                          'UNION '
                          'SELECT '
                          'failed.who, '
                          'success.success_count, '
                          'failed.failed_count '
                          'FROM ( '
                          'SELECT '
                          'assigned_to.who, '
                          'count(assigned_to.who) AS failed_count '
                          'FROM reports '
                          'JOIN assigned_to ON reports.bug_id = assigned_to.bug_id '
                          'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR '
                          'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR '
                          'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR '
                          'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR '
                          'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR '
                          'current_status == "VERIFIED" AND reports.current_resolution == "INVALID" '
                          'GROUP BY assigned_to.who) AS failed '
                          'LEFT OUTER JOIN ( '
                          'SELECT '
                          'assigned_to.who, '
                          'count(assigned_to.who) AS success_count '
                          'FROM reports '
                          'JOIN assigned_to ON reports.bug_id = assigned_to.bug_id '
                          'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR '
                          'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR '
                          'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR '
                          'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR '
                          'current_status == "CLOSED" AND reports.current_resolution == "FIXED" '
                          'GROUP BY assigned_to.who '
                          ') AS success '
                          'ON success.who = failed.who '
                          ') AS repRate '
                          ') INNER JOIN reports ON reports.reporter = who '
                          'ORDER BY reports.bug_id')

# 4.  What impact do bug reassignments have on the likelihood of a bug being fixed?
# list with nr of bugs which were successful and assignments for each reassingments
REASSINGMENTS = ('SELECT '
                 'bugSuccessRate, '
                 'bug_id '
                 'FROM ( '
                 'SELECT '
                 'assigned_to.bug_id, '
                 'count(assigned_to.bug_id) AS reassignments '
                 'FROM assigned_to '
                 'GROUP BY assigned_to.bug_id '
                 ') AS nrOfAssignmentsPerBug '
                 'JOIN ( '
                 'SELECT '
                 's1.nr_assignments, '
                 's1.nrSuccessReassignments, '
                 'f1.nrFailedReasignments, '
                 '(s1.nrSuccessReassignments * 1.0 / (s1.nrSuccessReassignments + f1.nrFailedReasignments)) AS bugSuccessRate '
                 'FROM (SELECT '
                 'success.nr_assignments, '
                 'count(success.nr_assignments) AS nrSuccessReassignments '
                 'FROM (SELECT '
                 'reports.bug_id, '
                 'a1.nr_assignments '
                 'FROM reports '
                 'JOIN (SELECT '
                 'bug_id, '
                 'count(bug_id) AS nr_assignments '
                 'FROM assigned_to '
                 'GROUP BY bug_id) a1 ON reports.bug_id = a1.bug_id '
                 'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR '
                 'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR '
                 'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR '
                 'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR '
                 'current_status == "CLOSED" AND reports.current_resolution == "FIXED" '
                 ') AS success '
                 'GROUP BY success.nr_assignments) AS s1 '
                 'JOIN ( '
                 'SELECT '
                 'fail.nr_assignments, '
                 'count(fail.nr_assignments) AS nrFailedReasignments '
                 'FROM (SELECT '
                 'reports.bug_id, '
                 'a2.nr_assignments '
                 'FROM reports '
                 'JOIN (SELECT '
                 'bug_id, '
                 'count(bug_id) AS nr_assignments '
                 'FROM assigned_to '
                 'GROUP BY bug_id) a2 ON reports.bug_id = a2.bug_id '
                 'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR '
                 'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR '
                 'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR '
                 'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR '
                 'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR '
                 'current_status == "VERIFIED" AND reports.current_resolution == "INVALID" '
                 ') AS fail '
                 'GROUP BY fail.nr_assignments) f1 ON s1.nr_assignments = f1.nr_assignments '
                 ') ON nr_assignments = nrOfAssignmentsPerBug.reassignments')

# 5. Number of reopenings per bug
REOPENINGS = ('SELECT bug_status.bug_id, bug_status.timestamp, COUNT(bug_status.id) AS count '
              'FROM bug_status '
              'WHERE bug_status.what = "REOPENED" '
              'GROUP BY bug_id '
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

# 8. relationship between reporter and users in cc
RELATIONSHIP = ('SELECT suc.sucessRate, rcc.bug_id '
                'FROM (SELECT reporter, what, reports.bug_id '
                'FROM cc '
                'JOIN reports ON reports.bug_id=cc.bug_id) AS rcc '
                'JOIN ( '
                'SELECT success.reporter, fail.what, success.nrSuccess, fail.nrFail, (success.nrSuccess*1.0/(success.nrSuccess+fail.nrFail)) AS sucessRate '
                'FROM ( SELECT reporter, what, count(cc.bug_id) AS nrSuccess '
                'FROM cc '
                'JOIN reports ON reports.bug_id=cc.bug_id '
                'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR '
                'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "FIXED" '
                'GROUP BY reporter, cc.what) success '
                'LEFT OUTER JOIN ( '
                'SELECT reporter, what, count(cc.bug_id) AS nrFail '
                'FROM cc '
                'JOIN reports ON reports.bug_id=cc.bug_id '
                'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "INVALID" '
                'GROUP BY reporter, cc.what) fail ON fail.reporter=success.reporter AND success.what=fail.what '
                'UNION '
                'SELECT success.reporter, fail.what, success.nrSuccess, fail.nrFail, (success.nrSuccess*1.0/(success.nrSuccess+fail.nrFail)) AS sucessRate '
                'FROM ( SELECT reporter, what, count(cc.bug_id) AS nrFail '
                'FROM cc '
                'JOIN reports ON reports.bug_id=cc.bug_id '
                'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "INVALID" '
                'GROUP BY reporter, cc.what) fail '
                'LEFT OUTER JOIN ( '
                'SELECT reporter, what, count(cc.bug_id) AS nrSuccess '
                'FROM cc '
                'JOIN reports ON reports.bug_id=cc.bug_id '
                'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR '
                'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR '
                'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR '
                'current_status == "CLOSED" AND reports.current_resolution == "FIXED" '
                'GROUP BY reporter, cc.what) success ON fail.reporter=success.reporter AND success.what=fail.what '
                ') AS suc '
                'ON rcc.reporter=suc.reporter AND rcc.what=suc.what; '
                )

# 9. relation of software version  and bug fix
SOFTWARE_VERSION = (
    'SELECT success.what, success.v_nr, success.bugsPerVersion, fail.bugsPerVersion, (success.bugsPerVersion*1.0/(success.bugsPerVersion+fail.bugsPerVersion)) AS bugSuccessRatePerVersion'
    'FROM (SELECT v1.what, v1.v_nr, ifnull(count(reports.bug_id), 0) AS bugsPerVersion'
    'FROM reports JOIN (SELECT prod.bug_id, prod.what, version.what AS v_nr'
    'FROM ( SELECT DISTINCT bug_id, what'
    'FROM version) AS version'
    'JOIN product prod ON prod.bug_id=version.bug_id) v1 ON reports.bug_id = v1.bug_id'
    'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR'
    'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR'
    'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR'
    'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR'
    'current_status == "CLOSED" AND reports.current_resolution == "FIXED"'
    'GROUP BY v1.what, v1.v_nr'
    ')  AS success'
    'JOIN ('
    'SELECT v1.what, v1.v_nr, ifnull(count(reports.bug_id), 0) AS bugsPerVersion'
    'FROM reports'
    'JOIN (SELECT prod.bug_id, prod.what, version.what AS v_nr'
    'FROM (SELECT DISTINCT bug_id, what'
    'FROM version) AS version'
    'JOIN product prod ON prod.bug_id=version.bug_id) v1 ON reports.bug_id = v1.bug_id'
    'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR'
    'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR'
    'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR'
    'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR'
    'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR'
    'current_status == "VERIFIED" AND reports.current_resolution == "INVALID"'
    'GROUP BY v1.what, v1.v_nr'
    ')  AS fail'
    'ON fail.what=success.what AND fail.v_nr=success.v_nr;'
)

# 10. calculates the influence of a bug relation to user interface, environment and network.

BUGNATURE = (
    'SELECT success.category, success.nrSuccessPerCategory, fail.nrFailsPerCategory, (nrSuccessPerCategory*1.0/(nrSuccessPerCategory+nrFailsPerCategory)) AS successRate'
    'FROM (SELECT cat.category, count(cat.bug_id) AS nrSuccessPerCategory'
    'FROM reports'
    'JOIN (SELECT bug_id,  "user_interface" AS category'
    'FROM short_desc'
    'WHERE short_desc.what LIKE "%user interface%"'
    'UNION'
    'SELECT bug_id,  "environment" AS category'
    'FROM short_desc'
    'WHERE short_desc.what LIKE "%environment%"'
    'UNION'
    'SELECT bug_id,  "network" AS category'
    'FROM short_desc'
    'WHERE short_desc.what LIKE "%network%") AS cat ON reports.bug_id=cat.bug_id'
    'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WORKSFORME" OR'
    'current_status == "RESOLVED" AND reports.current_resolution == "FIXED" OR'
    'current_status == "VERIFIED" AND reports.current_resolution == "FIXED" OR'
    'current_status == "CLOSED" AND reports.current_resolution == "WORKSFORME" OR'
    'current_status == "CLOSED" AND reports.current_resolution == "FIXED"'
    'GROUP BY cat.category) success'
    'JOIN ('
    'SELECT cat.category, count(cat.bug_id) AS nrFailsPerCategory'
    'FROM reports'
    'JOIN (SELECT bug_id,  "user_interface" AS category'
    'FROM short_desc'
    'WHERE short_desc.what LIKE "%user interface%"'
    'UNION'
    'SELECT bug_id,  "environment" AS category'
    'FROM short_desc'
    'WHERE short_desc.what LIKE "%environment%"'
    'UNION'
    'SELECT bug_id,  "network" AS category'
    'FROM short_desc'
    'WHERE short_desc.what LIKE "%network%") AS cat ON reports.bug_id=cat.bug_id'
    'WHERE current_status == "RESOLVED" AND reports.current_resolution == "WONTFIX" OR'
    'current_status == "RESOLVED" AND reports.current_resolution == "INVALID" OR'
    'current_status == "CLOSED" AND reports.current_resolution == "WONTFIX" OR'
    'current_status == "CLOSED" AND reports.current_resolution == "INVALID" OR'
    'current_status == "VERIFIED" AND reports.current_resolution == "WONTFIX" OR'
    'current_status == "VERIFIED" AND reports.current_resolution == "INVALID"'
    'GROUP BY cat.category) fail ON success.category=fail.category;'
)
