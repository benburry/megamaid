megamaid
========

Hacky, nonrobust, little-bit-noddy, potentially destructive tool for running a configurable PostgreSQL vacuum schedule against named tables in your database. Use in production at your own risk. We do.

Usage
-----
do\_vacuum.py is the place to look for an example implementation. You need to call the _megamaid.vacuum_ function with the target database name and a schedule for the tables you want vacuumed on each day of the week. The vacuum schedule format is described in megamaid.py

Once you have a schedule you're happy with, slap it in cron, redirecting stdout somewhere useful (perhaps somewhere that pgfouine can get to)

Important
---------
Note that megamaid expects the _psql_ and _vaccumdb_ binaries to be on your path, and requiring no username/password to access your database. 
Also, the megamaid.REMAINING\_TABLES function currently only works for tables in the _public_ schema

Disclaimers
-----------
This works for us, but it might well not work for you. I accept no responsibility if this does terrible, terrible things to your database.

All credit to @barn for naming
