import os
import psycopg2
from flask import Flask, request

app = Flask(__name__)

conn = psycopg2.connect(
    host="postgres.railway.internal",
    user="postgres",
    password="MMFkuYbxbnytTTTJERqNpGPlaSinIzwz",
    dbname="railway",
    port=5432
)

@app.route("/add_code", methods=["POST"])
def add_code():
    data = request.json
    code = data.get("code")
    uuid = data.get("uuid")
    if not code or not uuid:
        return "ERROR: Missing code or uuid", 400
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO codes(code, uuid) VALUES(%s, %s) ON CONFLICT DO NOTHING",
                (code, uuid)
            )
    return "OK"

@app.route("/check_code", methods=["GET"])
def check_code():
    code = request.args.get("code")
    if not code:
        return "ERROR: Missing code param", 400
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT telegram_id, uuid FROM codes WHERE code=%s AND used=true", (code,))
            row = cur.fetchone()
            if row:
                telegram_id, uuid = row
                return {"telegram_id": telegram_id, "uuid": uuid}
            return {"status": "NONE"}

@app.route("/remove_code", methods=["POST"])
def remove_code():
    data = request.json
    code = data.get("code")
    if not code:
        return "ERROR: Missing code", 400
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM codes WHERE code=%s", (code,))
    return "OK"
