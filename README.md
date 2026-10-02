# LLM SQL analyst agent

An analytics agent that turns natural-language questions into safe SQL queries and runs them against a real database.

The project is an example of how to build a tool-using LLM agent with schema grounding, safety guardrails, and execution against a real database.

## What it does

1. Takes a question in plain English.
2. Uses an LLM to generate a SQLite `SELECT` query.
3. Runs safety checks so only read-only SQL gets through.
4. Executes the query on a real database.
5. Returns the results to the user.

## Dataset

The agent runs on the Chinook SQLite database. Its tables include customers, invoices, tracks, albums, and artists. It is a realistic business-style schema that people use for SQL training and demos.

## What the project covers

- LLM and tool integration
- Schema-aware SQL generation
- Safety guardrails for AI systems
- Analytics on a real database, not mock data
- Development with enterprise constraints in mind

## Tech stack

- Python
- SQLite
- OpenAI API
- Pandas

## Project structure
```text
llm-sql-analyst-agent/
├── assets/
│   └── demo_customers.png
├── db/
│   └── chinook.db
├── src/
│   ├── agent.py        # LLM → SQL → execute (entry point)
│   ├── db.py           # SQL execution (opens DB read-only)
│   ├── schema.py       # Schema extraction
│   ├── safety.py       # SQL guardrails (sqlparse-based)
│   ├── prompt.py       # LLM instructions
│   └── config.py       # Paths, model, key validation
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Demo

### Top 10 countries by customers
![Top 10 Countries by Customers](assets/demo_customers.png)

## Setup

```bash
# 1. Clone and enter the repo
git clone https://github.com/FaridoonFarahi/llm-sql-analyst-agent.git
cd llm-sql-analyst-agent

# 2. Create a virtualenv
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install deps
pip install -r requirements.txt

# 4. Configure your OpenAI key
cp .env.example .env        # then edit .env and paste your key
```

The `.env` file is gitignored. Never commit your API key.

## How to run
```bash
python src/agent.py
```

The script asks for a natural-language question, then prints the generated SQL and the top rows of the result.

## Safety model

- The LLM never executes SQL itself. It only returns a SQL string.
- `sqlparse` parses that string, and the agent rejects anything that isn't a single `SELECT` (or `WITH … SELECT`).
- The SQLite connection is opened in read-only mode (`?mode=ro`), so even if the safety check were bypassed, the database file cannot be modified.
