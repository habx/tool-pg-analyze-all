#!/usr/bin/env python3

"""Analyzing all databases"""

import logging
import argparse
import os
from typing import Any, List
import psycopg2
from psycopg2.extras import RealDictCursor


def analyze_database(args: argparse.Namespace, dbname: str):
    """Analyze database"""

    logging.info("Analyzing database %s", dbname)
    conn = psycopg2.connect(dbname=dbname, user=args.username, password=args.password, host=args.host, port=args.port,
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


def analyze_everything(args: argparse.Namespace):
    """Analyze everything"""
    conn = psycopg2.connect(dbname=args.database, user=args.username,
                            password=args.password, host=args.host, port=args.port)
    cur = conn.cursor()
    cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    logging.info("Listing all databases")
    for row in cur.fetchall():
        dbname = row[0]
        if dbname not in args.exclude:
            analyze_database(args, dbname)


def parse_args(args: List[str] = None) -> Any:
    """Parse arguments"""
    parser = argparse.ArgumentParser(description='Process all database statistics')
    parser.add_argument('-H', '--host', help='Database host', default='localhost')
    parser.add_argument('-d', '--database',
                        help='Database name', default='postgres')
    parser.add_argument('-p', '--port', help='Database port', default='5432')
    parser.add_argument('-U', '--username', help='Database user',
                        default=os.getenv('USER', 'postgres'))
    parser.add_argument('-P', '--password', help='Database password', default='')
    parser.add_argument('-e', '--exclude', help='Exclude databases',
                        nargs='+', default=['rdsadmin', 'postgres'])
    parser.add_argument('-r', '--reindex',
                        help='Reindex databases', action='store_true')

    args = parser.parse_args(args) if args else parser.parse_args()

    if not args.password:
        args.password = os.getenv('PGPASSWORD', '')

    return args


def main():
    """Main function"""
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
    args = parse_args()
    analyze_everything(args)


if __name__ == '__main__':
    main()
