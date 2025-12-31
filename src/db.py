import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "db" / "chinook.db"

def run_sql(query: str) -> pd.DataFrame:
    """
    Runs a SQL query against the local Chinook SQLite database
    and returns a pandas DataFrame.
    """
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)
