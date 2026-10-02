import sqlite3
import pandas as pd

from config import DB_PATH


def run_sql(query: str) -> pd.DataFrame:
    """
    Run a single SQL query against the local Chinook SQLite database
    and return the result as a pandas DataFrame.

    Opens the DB in read-only mode (URI 'mode=ro') as a second layer of
    protection behind the safety check in safety.py.
    """
    uri = f"file:{DB_PATH}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        return pd.read_sql_query(query, conn)
