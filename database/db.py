import sqlite3
import re


def create_connection():
    return sqlite3.connect("database/sample.db")


def create_table():
    conn = create_connection()
    conn.commit()
    conn.close()


# 🔥 Get all tables
def get_all_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall() if t[0] != "sqlite_sequence"]

    conn.close()
    return tables


# 🔥 Get relationships (JOIN logic)
def get_relationships():
    conn = create_connection()
    cursor = conn.cursor()

    tables = get_all_tables()
    relationships = []

    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        fks = cursor.fetchall()

        for fk in fks:
            relationships.append({
                "table": table,
                "from": fk[3],
                "to_table": fk[2],
                "to": fk[4]
            })

    conn.close()
    return relationships


# 🔥 Execute query
def run_query(query):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # ✅ Always use execute() — executescript() skips cursor.description
        query = query.strip().rstrip(";")
        cursor.execute(query)

        if cursor.description:
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return {"data": results, "columns": columns}
        else:
            conn.commit()
            return {"message": "✅ Query executed successfully"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()


# 🔥 Dangerous query detection with word boundaries (no false positives)
def is_dangerous(query):
    keywords = ["delete", "drop", "update", "insert"]
    pattern = r'\b(' + '|'.join(keywords) + r')\b'
    return bool(re.search(pattern, query.lower()))