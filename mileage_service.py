"""
mileage_service.py
Handles mileage maths + SQLite persistence.
"""

import sqlite3
from contextlib import closing
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/mileage.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DDL = """
CREATE TABLE IF NOT EXISTS mileage_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT,
    odo_start REAL,
    odo_end   REAL,
    litres    REAL,
    distance  REAL,
    mileage   REAL,
    cost_per_litre REAL,
    total_cost REAL,
    cost_per_km REAL
);
"""

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ―― initialise on import ――――――――――――――――――――――――――――――――――――――――
with closing(_connect()) as c:
    c.executescript(DDL)
    c.commit()

# ―― core business logic ――――――――――――――――――――――――――――――――――――――――――
def calc_metrics(start, end, litres, price):
    distance = end - start
    mileage = round(distance / litres, 2)
    total_cost = round(litres * price, 2)
    cost_per_km = round(total_cost / distance, 2)
    return distance, mileage, total_cost, cost_per_km

def save_log(start, end, litres, price):
    distance, mileage, total_cost, cost_per_km = calc_metrics(start, end, litres, price)
    with closing(_connect()) as c:
        c.execute(
            """
            INSERT INTO mileage_log
            (ts, odo_start, odo_end, litres, distance, mileage,
             cost_per_litre, total_cost, cost_per_km)
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                datetime.now().isoformat(timespec="seconds"),
                start, end, litres, distance, mileage,
                price, total_cost, cost_per_km,
            ),
        )
        c.commit()
    return distance, mileage, total_cost, cost_per_km

def fetch_log():
    with closing(_connect()) as c:
        cur = c.execute("SELECT * FROM mileage_log ORDER BY id DESC")
        return cur.fetchall()
