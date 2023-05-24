"""
TODO
"""

from psycopg2.extensions import cursor

# from utils import parse_int


def populate_chips(cur: cursor, rows: list[dict[str, str]]):
    """
    TODO
    """
    for row in rows:
        chip = (
            row["Product"],
            row["Type"],
            row["Release Date"],
            row["Process Size (nm)"],
            row["TDP (W)"],
            row["Transistors (million)"],
            row["Freq (MHz)"],
            row["Vendor"],
        )
        cur.execute(
            """
            insert into chip(product, the_type, release_date, process_size, tdp, transistors, frequency, Vendor) 
            values(%s, %s, %s, %s, %s, %s, %s, %s) 
            on conflict do nothing
            """,
            chip,
        )
