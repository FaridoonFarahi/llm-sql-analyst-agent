import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "db" / "chinook.db"

def get_schema() -> pd.DataFrame:
    """
    Returns table + column info for every table in the database.
    """
    with sqlite3.connect(DB_PATH) as conn:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;",
            conn
        )

        rows = []
        for t in tables["name"]:
            cols = pd.read_sql_query(f"PRAGMA table_info({t});", conn)
            for _, r in cols.iterrows():
                rows.append({
                    "table": t,
                    "column": r["name"],
                    "type": r["type"]
                })

        return pd.DataFrame(rows)
