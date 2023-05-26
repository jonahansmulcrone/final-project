import math
from flask import Flask, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
    cursor_factory=RealDictCursor)
app = Flask(__name__)


def parse_int_list(value, valid_values, default_value):
    try:
        int_value = int(value)
        for v in valid_values:
            if v == int_value:
                return v
        return default_value
    except:
        return default_value
    
def parse_int_in_range(value, min_value, max_value, default_value):
    try:
        parsed = int(value)
        if parsed < min_value or parsed > max_value:
            return default_value
        return parsed
    except:
        return default_value

SORT_DIR = ["asc", "desc"]
SORT_BY = ["product", "the_type", "process_size", "transistors", "tdp", "frequency", "release_date"]

@app.route("/")
def hello_world():
    name = request.args.get("name", "World")
    return f"<p>Hello, {name}!</p>"


@app.route("/chips")
def render_sets():
    product = request.args.get("product", "")
    the_type = request.args.get("the_type", "")
    release_date = request.args.get("release_date", "")
    process_size = request.args.get("process_size", "")
    tdp = request.args.get("tdp", "")
    transistors = request.args.get("transistors", "")
    frequency = request.args.get("frequency", "")
    vendor = request.args.get("vendor", "")
    sort_by = request.args.get("sort_by", "product")
    sort_dir = request.args.get("sort_dir", "asc")
    page = request.args.get("page", 1, type=int)
    results_per_page = parse_int_list(request.args.get("results_per_page"), [10, 50, 100], 10)

    from_where_clause = """
    from chip c
    where c.product ilike %(product)s
    and c.the_type ilike %(the_type)s 
    and c.vendor ilike %(vendor)s
    """

    params = {
        "product": f"%{product}%",
        "the_type": f"%{the_type}",
        "release_date": f"%{release_date}%",
        "process_size": f"%{process_size}%",
        "tdp": f"%{tdp}%",
        "transistors": f"%{transistors}%",
        "frequency": f"%{frequency}%",
        "vendor": f"%{vendor}%",
        "limit": f"{results_per_page}",
        "page": f"{page}",
        "offset": f"{((page-1)*results_per_page)}"
    }

    with conn.cursor() as cur:
        cur.execute(f"""
                    select c.product as product, c.the_type as the_type, 
                    c.release_date as release_date, c.process_size as process_size, 
                    c.tdp as tdp, c.transistors as transistors,
                    c.frequency as frequency, c.vendor as vendor
                    {from_where_clause}
                    order by {sort_by} {sort_dir}
                    limit %(limit)s
                    offset %(offset)s
                    """, params)
        
        results = list(cur.fetchall())

        cur.execute(f"select count(*) as count {from_where_clause}",
                    params)
        count = cur.fetchone()["count"]

        total_pages = math.ceil(count / results_per_page)

        def get_sort_dir(col):
            if col == sort_by:
                return "desc" if sort_dir == "asc" else "asc"
            return "asc"

        return render_template("chips.html",
                               params=request.args,
                               result_count=count,
                               chips=results,
                               get_sort_dir=get_sort_dir,
                               total_pages=total_pages)