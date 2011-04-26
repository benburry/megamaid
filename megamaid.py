import subprocess
import sys
from datetime import date, datetime

_DBNAME = None
_TABLE_CONFIG = None

def REMAINING_TABLES():
    remainingtables = []
    existingtables = []
    for tables in _TABLE_CONFIG.values():
        for item in tables:
            existingtables.append(item)
                
    p = subprocess.Popen(['psql', '-t', '-A', '-c', "select tablename as table from pg_tables where schemaname = 'public' order by tablename", '-d', _DBNAME], stdout=subprocess.PIPE)
    for line in p.stdout:
        table = line.strip()
        if table not in existingtables:
            remainingtables.append(table)
            
    return remainingtables

def report(logline):
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), logline
    sys.stdout.flush()

def dedupe(seq): 
    seen = {}
    result = []
    for item in seq:
        if item in seen: continue
        seen[item] = 1
        result.append(item)
    return result
  
def vacuum_table(database, tablename, dryrun=False):
    report("Starting vacuum of table %s in database %s" % (tablename, database))
    if not dryrun:
        subprocess.call(['vacuumdb', '-d', database, '-t', tablename, '-z', '-v'], stderr=subprocess.STDOUT)
    else:
        report("Skipped - dryrun mode")
    report("Completed vacuum of table %s in database %s" % (tablename, database))
  
# table_config is a hash of tables to be vacuumed for each day, of the form
#   days : tables
#   where 'days' is an iterable of 0-indexed days, 0 being monday
#   and 'tables' is an iterable of table names
#
# TABLES_BY_DAY = {
#     (0,2,4)     : [
#         'table1',
#         'table2',
#     ],
#     (1,3,6)     : [
#         'table3',
#         'table1',
#         'table4',
#     ],
#     (5)         : [
#         megamaid.REMAINING_TABLES,          # this is special. it means 'the rest'
#     ],
# }

def vacuum(day_index=date.weekday(datetime.now()), database=None, table_config={}, dryrun=False):
    #ugh
    global _DBNAME
    global _TABLE_CONFIG
    _DBNAME=database
    _TABLE_CONFIG=table_config
    
    tables_to_vac = []
    report("vacuum for day index %s against database %s" % (day_index, database))

    for days, tables_for_day in table_config.iteritems():
        if not hasattr(days, '__iter__'): days = [days]
        if day_index in days: 
            for item in tables_for_day:
                if callable(item):
                    tables_to_vac.extend(item())
                else:
                    tables_to_vac.append(item)
    
    tables_to_vac = dedupe(tables_to_vac)
    report("vacuum queue is %s" % tables_to_vac)
  
    for table in tables_to_vac:
        if table is not None and dryrun is not True: vacuum_table(database, table, dryrun)

