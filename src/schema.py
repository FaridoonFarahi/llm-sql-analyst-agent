import sqlite3
import pandas as pd

from config import DB_PATH


def get_schema() -> pd.DataFrame:
    """
    Return one row per (table, column) for every table in the database.
    Used to ground the LLM in the real schema.
    """
    uri = f"file:{DB_PATH}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;",
            conn,
        )

        rows = []
        for t in tables["name"]:
            cols = pd.read_sql_query(f"PRAGMA table_info({t});", conn)
            for _, r in cols.iterrows():
                rows.append({
                    "table": t,
                    "column": r["name"],
                    "type": r["type"],
                })

        return pd.DataFrame(rows)
