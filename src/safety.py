import re

def is_safe_sql(sql: str) -> bool:
    """
    Very simple safety rule:
    - Must start with SELECT (or WITH ... SELECT)
    - Must not contain dangerous keywords
    """
    s = sql.strip().lower()

    # Allow SELECT or WITH (CTE)
    if not (s.startswith("select") or s.startswith("with")):
        return False

    # Block dangerous operations
    banned = r"\b(drop|delete|update|insert|alter|truncate|create|replace|attach|detach|pragma)\b"
    if re.search(banned, s):
        return False

    return True
