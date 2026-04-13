import ollama
from database.db import get_schema

def generate_sql(user_query):

    schema = get_schema()

    prompt = f"""
You are an expert SQL generator.

Database schema:
{schema}

Rules:
- Only output SQL query
- No explanation
- Use correct table and column names

User query: {user_query}
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response['message']['content']

    # 🔥 Clean output
    sql = sql.replace("`", "").strip()
    sql = sql.split("\n")[0]

    return sql