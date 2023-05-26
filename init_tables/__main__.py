"""
Entrypoint to module that will initialize and populate the Lego catalog database.
"""
import csv

import psycopg2

from populate_task import POPULATE_TASKS


with psycopg2.connect("host=db dbname=postgres user=postgres password=postgres") as conn:
    for schema_file_path, csv_file_path, parse_and_insert_fn in POPULATE_TASKS:
        with conn.cursor() as cur:
            with open(schema_file_path, encoding="utf8") as schema_file:
                cur.execute(schema_file.read())
            print(f"executed schema file {schema_file_path}")
            with open(csv_file_path, encoding="utf8") as csv_file:
                rows = list(csv.DictReader(csv_file))
                parse_and_insert_fn(cur, rows)
            print(f"processed {csv_file_path}")
print("finished initializing database")
