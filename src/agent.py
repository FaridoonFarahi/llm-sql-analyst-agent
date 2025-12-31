import os
import pandas as pd
from openai import OpenAI

from db import run_sql
from schema import get_schema
from safety import is_safe_sql
from prompt import SYSTEM_PROMPT

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def schema_to_text(schema_df: pd.DataFrame) -> str:
    """
    Turn schema DataFrame into a text block the LLM can read.
    """
    lines = []
    for table in schema_df["table"].unique():
        cols = schema_df[schema_df["table"] == table]
        col_list = ", ".join([f"{r.column} ({r.type})" for r in cols.itertuples(index=False)])
        lines.append(f"- {table}: {col_list}")
    return "\n".join(lines)

def generate_sql(user_question: str) -> str:
    schema_df = get_schema()
    schema_text = schema_to_text(schema_df)

    user_prompt = f"""
SCHEMA:
{schema_text}

QUESTION:
{user_question}

Return ONLY a single SQLite SELECT query:
""".strip()

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0
    )

    sql = resp.choices[0].message.content.strip()
    return sql

def answer_question(user_question: str):
    sql = generate_sql(user_question)

    if not is_safe_sql(sql):
        raise ValueError(f"Unsafe SQL generated:\n{sql}")

    df = run_sql(sql)
    return sql, df

if __name__ == "__main__":
    question = input("Ask a question about the Chinook database: ").strip()
    sql, df = answer_question(question)

    print("\n--- Generated SQL ---")
    print(sql)

    print("\n--- Results (top 20 rows) ---")
    print(df.head(20))
