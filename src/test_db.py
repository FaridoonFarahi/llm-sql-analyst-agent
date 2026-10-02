from db import run_sql

query = """
SELECT
  c.country,
  COUNT(*) AS num_customers
FROM customers c
GROUP BY c.country
ORDER BY num_customers DESC
LIMIT 10;
"""

print(run_sql(query))
