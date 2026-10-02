"""
SQL safety check.

Uses sqlparse to identify statement types. Allows exactly one
read-only statement (SELECT or WITH ... SELECT). Falls back to a regex
check if sqlparse is unavailable.
"""
from __future__ import annotations

import re

try:
    import sqlparse
    _HAS_SQLPARSE = True
except ImportError:  # pragma: no cover
    _HAS_SQLPARSE = False


_BANNED_KEYWORDS = {
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE",
    "CREATE", "REPLACE", "ATTACH", "DETACH", "PRAGMA", "VACUUM",
    "REINDEX", "ANALYZE", "GRANT", "REVOKE",
}


def _is_safe_sqlparse(sql: str) -> bool:
    statements = [s for s in sqlparse.parse(sql) if s.tokens and str(s).strip()]

    # Require exactly one statement (blocks "SELECT 1; DROP TABLE x").
    if len(statements) != 1:
        return False

    stmt = statements[0]

    # First meaningful token must be SELECT or WITH. sqlparse tags WITH as
    # Token.Keyword.CTE (a subtype of Keyword), so we check the normalized
    # value rather than strict ttype equality.
    first = stmt.token_first(skip_cm=True)
    if first is None:
        return False
    if first.normalized.upper() not in ("SELECT", "WITH"):
        return False

    # Walk every token; reject if any banned keyword appears outside string/comment.
    for token in stmt.flatten():
        if token.is_keyword and token.normalized.upper() in _BANNED_KEYWORDS:
            return False

    return True


def _is_safe_regex(sql: str) -> bool:
    s = sql.strip().lower()
    if not (s.startswith("select") or s.startswith("with")):
        return False
    banned = r"\b(drop|delete|update|insert|alter|truncate|create|replace|attach|detach|pragma|vacuum|reindex|grant|revoke)\b"
    if re.search(banned, s):
        return False
    return True


def is_safe_sql(sql: str) -> bool:
    """
    True if `sql` is a single read-only statement starting with SELECT or WITH
    and containing no banned keywords (DDL, DML writes, PRAGMA, attach, etc.).
    """
    if not isinstance(sql, str) or not sql.strip():
        return False
    if _HAS_SQLPARSE:
        return _is_safe_sqlparse(sql)
    return _is_safe_regex(sql)
