# PG all tables analysis tool

## Why

This tool generates the table statistics after a PG upgrade. 
It only does so for tables that have never been analyzed before.

## How

Sample usage:
```shell
PGPASSWORD=xxx ./main.py -H database -U dbadmin
```

Help:
```shell
./main.py --help
usage: main.py [-h] [-H HOST] [-d DATABASE] [-p PORT] [-U USERNAME] [-e EXCLUDE [EXCLUDE ...]] [-r]

Process all database statistics

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Database host
  -d DATABASE, --database DATABASE
                        Database name
  -p PORT, --port PORT  Database port
  -U USERNAME, --username USERNAME
                        Database user
  -e EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        Exclude databases
  -r, --reindex         Reindex databases
```