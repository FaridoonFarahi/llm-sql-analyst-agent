import sqlite3
import pandas as pd

from config import DB_PATH


def get_schema() -> pd.DataFrame:
    """
    Return one row per (table, column) for every table in the database.
    The agent puts this in the prompt so the LLM sees the real schema.
    """
    uri = f"file:{DB_PATH}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;",
            conn,
        )

        rows = []
        for table in tables["name"]:
            cols = pd.read_sql_query(f"PRAGMA table_info({table});", conn)
            for _, col in cols.iterrows():
                rows.append({
                    "table": table,
                    "column": col["name"],
                    "type": col["type"],
                })

        return pd.DataFrame(rows)
