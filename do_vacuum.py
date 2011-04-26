#!/usr/bin/env python
import sys
import megamaid

#################################################################################
# CONFIGURABLE TABLE LIST
#
# Tables to be vacuumed for each day, of the form
#   days : tables
#   where 'days' is an iterable of 0-indexed days, 0 being monday
#   and 'tables' is an iterable of table names
#
TABLES_BY_DAY = {
    (0,2,4)     : [
        'table1',
        'table2',
    ],
    (1,3,6)     : [
        'table3',
        'table1',
        'table4',
    ],
    (5)         : [
        megamaid.REMAINING_TABLES,          # this is special. it means 'the rest'
    ],
}

DATABASE = 'mydatabase'

#################################################################################

def main(configdump=False, dryrun=False):
    if not configdump:
        megamaid.vacuum(database=DATABASE, table_config=TABLES_BY_DAY, dryrun=dryrun)
    else:
        for day in xrange(7):
            megamaid.vacuum(day_index=day, database=DATABASE, table_config=TABLES_BY_DAY, dryrun=True)
            
    return 0


if __name__ == '__main__':
    dryrun = False
    configdump = False
    if '--dryrun' in sys.argv or '-d' in sys.argv: dryrun = True
    if '--config' in sys.argv or '-c' in sys.argv: 
        configdump = True
        dryrun = True

    sys.exit(main(configdump, dryrun))
