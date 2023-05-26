"""
TODO
"""

from psycopg2.extensions import cursor

from utils import parse_int


def populate_parts(cur: cursor, rows: list[dict[str, str]]):
    """
    TODO
    """
    for row in rows:
        theme = (parse_int(row['id']), row['name'],
                 parse_int(row['parent_id']))
        cur.execute("""
            insert into theme(id, name, parent_id) 
            values(%s, %s, %s) 
            on conflict do nothing
            """, theme)
