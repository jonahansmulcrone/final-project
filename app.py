import psycopg2
from flask import Flask, request
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
    cursor_factory=RealDictCursor)
app = Flask(__name__)


@app.route("/")
def hello_world():
    first_name = request.args.get("first_name", "googly")
    last_name = request.args.get("last_name", "mcfoogly")
    return f"<h1>Hello, {first_name} {last_name}!</h1>"

@app.route("/api/chip")
def fetch_chip():
    with conn.cursor() as cur:
        cur.execute("select * from chip")
        result = list(cur.fetchall())

        return result
