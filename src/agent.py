"""
LLM SQL analyst agent.

Pipeline: a natural-language question goes to the LLM, which writes a
SELECT. The query passes a safety check, runs, and comes back as a DataFrame.
"""
from __future__ import annotations

from functools import lru_cache

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load .env once, before importing modules that touch the OpenAI client.
load_dotenv()

from config import MODEL, PREVIEW_ROWS, require_api_key
from db import run_sql
from prompt import SYSTEM_PROMPT
from safety import is_safe_sql
from schema import get_schema


class UnsafeSQLError(ValueError):
    """Raised when the LLM produces SQL that fails the safety check."""


def _client() -> OpenAI:
    return OpenAI(api_key=require_api_key())


@lru_cache(maxsize=1)
def _cached_schema_text() -> str:
    """Return the schema as prompt text. The schema doesn't change at runtime, so it is cached."""
    schema_df = get_schema()
    lines = []
    for table in schema_df["table"].unique():
        table_cols = schema_df[schema_df["table"] == table]
        col_list = ", ".join(f"{row.column} ({row.type})" for row in table_cols.itertuples(index=False))
        lines.append(f"- {table}: {col_list}")
    return "\n".join(lines)


def _strip_code_fence(sql: str) -> str:
    """Remove a ```sql ... ``` fence if the LLM wrapped its output in one."""
    text = sql.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[: -3]
    return text.strip().lstrip("sql").strip() if text.lower().startswith("sql\n") else text.strip()


def generate_sql(user_question: str, client: OpenAI | None = None) -> str:
    client = client or _client()
    schema_text = _cached_schema_text()

    user_prompt = (
        f"SCHEMA:\n{schema_text}\n\n"
        f"QUESTION:\n{user_question}\n\n"
        "Return ONLY a single SQLite SELECT query:"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    return _strip_code_fence(response.choices[0].message.content or "")


def answer_question(user_question: str, client: OpenAI | None = None) -> tuple[str, pd.DataFrame]:
    sql = generate_sql(user_question, client=client)
    if not is_safe_sql(sql):
        raise UnsafeSQLError(f"Unsafe SQL generated:\n{sql}")
    df = run_sql(sql)
    return sql, df


def _main() -> int:
    try:
        question = input("Ask a question about the Chinook database: ").strip()
        if not question:
            print("No question entered.")
            return 1

        sql, df = answer_question(question)

        print("\n--- Generated SQL ---")
        print(sql)
        print(f"\n--- Results (top {PREVIEW_ROWS} rows of {len(df)}) ---")
        print(df.head(PREVIEW_ROWS))
        return 0

    except RuntimeError as e:
        print(f"Config error: {e}")
        return 2
    except UnsafeSQLError as e:
        print(f"Refused: {e}")
        return 3
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(_main())
