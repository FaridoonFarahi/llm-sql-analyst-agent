# LLM SQL Analyst Agent

An AI-powered analytics agent that converts natural language questions into safe SQL queries and executes them against a real database.

This project demonstrates how to build a **tool-using LLM agent** with schema grounding, safety guardrails, and real database execution.

---

## 🔍 What This Agent Does

1. Takes a question in plain English  
2. Uses an LLM to generate a SQLite `SELECT` query  
3. Applies safety checks (read-only SQL only)  
4. Executes the query on a real database  
5. Returns results to the user  

**English → SQL → Execute → Results**

---

## 🗄 Dataset

- **Chinook SQLite Database**
- Tables include: customers, invoices, tracks, albums, artists
- Realistic business-style schema used for SQL training and demos

---

## 🧠 Why This Project Matters

This project showcases:
- LLM + tool integration
- Schema-aware SQL generation
- Safety guardrails for AI systems
- Real database analytics (not mock data)
- Enterprise-aware development constraints

---

## 🛠 Tech Stack

- Python
- SQLite
- OpenAI API
- Pandas

---

## 📂 Project Structure
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

---

## ▶️ Demo Screenshots

### Top 10 Countries by Customers
![Top 10 Countries by Customers](assets/demo_customers.png)

---

## 🛠 Setup

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

> The `.env` file is gitignored — never commit your API key.

---

## ▶️ How to Run
```bash
python src/agent.py
```

You'll be prompted for a natural-language question. The agent prints
the generated SQL and the top rows of the result.

---

## 🛡 Safety model

- **LLM never executes SQL directly.** It only emits a SQL string.
- That string is parsed by `sqlparse`. The agent **rejects** anything
  that isn't a single `SELECT` (or `WITH … SELECT`).
- The SQLite connection is opened in **read-only mode**
  (`?mode=ro`) so even if the safety check were bypassed,
  the database file cannot be modified.

---
