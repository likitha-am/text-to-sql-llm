import sqlite3
import re

# 🔗 Create connection
def create_connection():
    return sqlite3.connect("database/sample.db")


# 🏗️ Create tables (only for demo — optional in production)
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        city TEXT,
        UNIQUE(name, age, city)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount INTEGER,
        customer_id INTEGER
    )
    """)

    conn.commit()
    conn.close()


# 🧠 Get schema dynamically
def get_schema():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = ""

    for table in tables:
        table_name = table[0]

        # skip SQLite internal table
        if table_name == "sqlite_sequence":
            continue

        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        col_names = [col[1] for col in columns]

        schema += f"{table_name}({', '.join(col_names)})\n"

    conn.close()
    return schema


# ⚙️ Run SQL query (robust version)
def run_query(query):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        query = query.strip()

        # 🔥 REMOVE semicolon (VERY IMPORTANT)
        if query.endswith(";"):
            query = query[:-1]

        print("FINAL QUERY:", query)  # debug

        cursor.execute(query)

        # 🔥 THIS is the REAL check
        if cursor.description is not None:
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            return {
                "data": results,
                "columns": columns
            }

        else:
            conn.commit()
            return {"message": "✅ Query executed successfully"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()


# 🚨 Detect dangerous queries
def is_dangerous(query):
    keywords = ["delete", "drop", "update", "insert"]
    pattern = r'\b(' + '|'.join(keywords) + r')\b'
    return bool(re.search(pattern, query.lower()))


# 🧠 Extract table name dynamically
def extract_table_name(query):
    query = query.lower()

    match = re.search(r'(from|into|update)\s+(\w+)', query)

    if match:
        return match.group(2)

    return None

def get_all_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall() if t[0] != "sqlite_sequence"]

    conn.close()
    return tables


def get_table_schema(table_name):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    col_names = [col[1] for col in columns]

    conn.close()

    return f"{table_name}({', '.join(col_names)})"