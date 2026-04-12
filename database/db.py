import sqlite3

def create_connection():
    conn = sqlite3.connect("database/sample.db")
    return conn


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        city TEXT
    )
    """)

    # Insert sample data (only if empty)
    cursor.execute("SELECT COUNT(*) FROM customers")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany("""
        INSERT INTO customers (name, age, city) VALUES (?, ?, ?)
        """, [
            ('Alice', 25, 'New York'),
            ('Bob', 30, 'London'),
            ('Charlie', 35, 'Paris'),
            ('David', 40, 'London')
        ])

    conn.commit()
    conn.close()


def run_query(query):
    conn = create_connection()
    cursor = conn.cursor()

    # Safety check
    if any(word in query.lower() for word in ["drop", "delete", "update", "insert"]):
        return {"error": "❌ Unsafe query blocked!"}

    try:
        cursor.execute(query)

        results = cursor.fetchall()

        # 👇 THIS IS THE MAGIC
        column_names = [desc[0] for desc in cursor.description]

        return {
            "data": results,
            "columns": column_names
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()