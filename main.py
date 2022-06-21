#!/usr/bin/env python3

"""Analyzing all databases"""

import logging
import argparse
import os
import psycopg2
from psycopg2.extras import RealDictCursor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

parser = argparse.ArgumentParser(description='Process all database statistics')
parser.add_argument('-H', '--host', help='Database host', default='localhost')
parser.add_argument('-d', '--database',
                    help='Database name', default='postgres')
parser.add_argument('-p', '--port', help='Database port', default='5432')
parser.add_argument('-U', '--username', help='Database user',
                    default=os.getenv('USER', 'postgres'))
parser.add_argument('-e', '--exclude', help='Exclude databases',
                    nargs='+', default=['rdsadmin', 'postgres'])
parser.add_argument('-r', '--reindex',
                    help='Reindex databases', action='store_true')
password = os.getenv('PGPASSWORD', '')

args = parser.parse_args()


def analyze_database(dbname: str):
    """Analyze database"""

    logging.info("Analyzing database %s", dbname)
    conn = psycopg2.connect(dbname=dbname, user=args.username, password=password, host=args.host, port=args.port,
                            application_name='tool-pg-analyze-all')
    conn.set_session(autocommit=True)

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from pg_stat_user_tables")
    for row in cur.fetchall():
        if row['last_analyze'] is None and row['last_autoanalyze'] is None:
            logging.info("Analyzing table %s / %s.%s", dbname,
                         row['schemaname'], row['relname'])
            cur2 = conn.cursor()
            cur2.execute(
                f"vacuum analyze \"{row['schemaname']}\".\"{row['relname']}\"")

    if args.reindex:
        logging.info("Reindexing database %s", dbname)
        cur.execute("select pg_database_size(%s) as size", (dbname,))
        size_before = cur.fetchone()['size']
        cur.execute(f"reindex database \"{dbname}\"")
        cur.execute("select pg_database_size(%s) as size", (dbname,))
        size_after = cur.fetchone()['size']
        gain = (size_before - size_after) / size_before * 100
        logging.info(
            "Reindexed database %s, size before: %d, size after: %d, gain: %.2f%%",
            dbname,
            size_before,
            size_after,
            gain,
        )


def analyze_everything():
    """Analyze everything"""
    conn = psycopg2.connect(dbname=args.database, user=args.username,
                            password=password, host=args.host, port=args.port)
    cur = conn.cursor()
    cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    for row in cur.fetchall():
        dbname = row[0]
        if dbname not in args.exclude:
            analyze_database(dbname)


analyze_everything()
