import ollama
import re
from rag.retriever import build_schema_context


def generate_sql(user_query):

    schema = build_schema_context(user_query)

    prompt = f"""
You are an expert SQL generator.

Database schema:
{schema}

Rules:
- Output ONLY valid SQLite SQL, nothing else
- ALWAYS include a FROM clause
- If a column belongs to a table NOT in FROM, you MUST JOIN that table
- NEVER reference a column from a table that is not in FROM or JOIN
- Use the relationships listed above to write correct JOINs
- Prefer INNER JOIN
- No explanation, no markdown, no backticks

User query: {user_query}
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response['message']['content']

    # 🔥 Clean output
    sql = sql.strip()
    sql = re.sub(r"```.*?```", "", sql, flags=re.DOTALL)
    sql = re.sub(r"^sql", "", sql, flags=re.IGNORECASE).strip()

    match = re.search(r"(SELECT|INSERT|UPDATE|DELETE).*", sql, re.IGNORECASE | re.DOTALL)
    if match:
        sql = match.group(0)

    return sql.strip()