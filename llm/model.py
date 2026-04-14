from rag.retriever import build_schema_context
import ollama
import re

def generate_sql(user_query):

    schema = build_schema_context(user_query)

    prompt = f"""
You are a strict SQL generator.

Database schema:
{schema}

Rules:
- Output ONLY SQL
- No explanation
- Return all columns unless specified

User query: {user_query}
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response['message']['content']

    # cleaning
    sql = sql.strip()
    sql = re.sub(r"```.*?```", "", sql, flags=re.DOTALL)
    sql = re.sub(r"^sql", "", sql, flags=re.IGNORECASE).strip()

    match = re.search(r"(SELECT|INSERT|UPDATE|DELETE).*", sql, re.IGNORECASE)
    if match:
        sql = match.group(0)

    return sql.strip()