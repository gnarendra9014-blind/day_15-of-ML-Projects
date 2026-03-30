import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "pipeline.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""CREATE TABLE IF NOT EXISTS pipeline_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        status TEXT,
        attempt INTEGER,
        errors TEXT,
        fixes TEXT,
        rows_processed INTEGER
    )""")
    conn.commit()
    conn.close()

def log_run(status: str, attempt: int, errors: list, fixes: list, rows: int):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""INSERT INTO pipeline_runs
        (timestamp, status, attempt, errors, fixes, rows_processed)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (datetime.now().isoformat(), status, attempt,
         "|".join(errors), "|".join(fixes), rows)
    )
    conn.commit()
    conn.close()

def save_clean_data(df: pd.DataFrame):
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("clean_data", conn, if_exists="replace", index=False)
    conn.close()

def get_run_history():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM pipeline_runs ORDER BY id DESC LIMIT 10", conn)
    conn.close()
    return df