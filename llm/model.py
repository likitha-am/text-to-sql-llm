import ollama
from database.db import get_schema
import re

def generate_sql(user_query):

    schema = get_schema()

    prompt = f"""
You are a strict SQL generator.

Database schema:
{schema}

Rules:
- Output ONLY a valid SQLite query
- NO explanation
- NO markdown
- DO NOT write 'sql'
- Only one query
- Always return all columns unless user specifies specific fields

User query: {user_query}
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response['message']['content']

    print("RAW LLM OUTPUT:", sql)  # 🔥 terminal debug

    # 🔥 AGGRESSIVE CLEANING
    sql = sql.strip()

    # remove markdown
    sql = re.sub(r"```.*?```", "", sql, flags=re.DOTALL)

    # remove 'sql'
    sql = re.sub(r"^sql", "", sql, flags=re.IGNORECASE).strip()

    # extract valid query
    match = re.search(r"(SELECT|INSERT|UPDATE|DELETE).*", sql, re.IGNORECASE)
    if match:
        sql = match.group(0)

    return sql.strip()