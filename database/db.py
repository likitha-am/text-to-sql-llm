import sqlite3
import re

# 🔗 Create connection
def create_connection():
    return sqlite3.connect("database/sample.db")


# 🏗️ Create table ONLY (no auto insert ❌)
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        city TEXT,
        UNIQUE(name, age, city)  -- 🔥 prevents duplicates
    )
    """)

    conn.commit()
    conn.close()


# ⚙️ Run SQL query
def run_query(query):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        # ✅ SELECT queries
        if cursor.description:
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            return {
                "data": results,
                "columns": column_names
            }

        else:
            # ✅ INSERT / DELETE / UPDATE
            conn.commit()
            return {"message": "✅ Query executed successfully"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()


# 🚨 Detect dangerous queries (uses word boundaries to avoid false positives)
def is_dangerous(query):
    dangerous_keywords = ["delete", "drop", "update", "insert"]
    pattern = r'\b(' + '|'.join(dangerous_keywords) + r')\b'
    return bool(re.search(pattern, query.lower()))