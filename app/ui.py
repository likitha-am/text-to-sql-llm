import streamlit as st
import pandas as pd
import re

from llm.model import generate_sql
from database.db import create_table, run_query, is_dangerous, create_connection

st.set_page_config(page_title="Text-to-SQL", layout="centered")

st.title("💬 Ask Your Database")

create_table()

# ─────────────────────────────────────────
# 🔥 Upload MULTIPLE CSVs (each becomes its own table)
# ─────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Upload one or more CSV files (each becomes a table)",
    type=["csv"],
    accept_multiple_files=True  # ✅ allows multiple uploads
)

if uploaded_files:
    conn = create_connection()
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file)
        table_name = uploaded_file.name.replace(".csv", "").replace(" ", "_").replace("-", "_")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        st.success(f"✅ Uploaded as table: `{table_name}` ({len(df)} rows, columns: {', '.join(df.columns)})")
    conn.close()

# ─────────────────────────────────────────
# 🔥 Session state
# ─────────────────────────────────────────
if "sql_query" not in st.session_state:
    st.session_state.sql_query = None

if "executed" not in st.session_state:
    st.session_state.executed = False

if "result" not in st.session_state:
    st.session_state.result = None

# ─────────────────────────────────────────
# 🔥 Query input
# ─────────────────────────────────────────
user_input = st.text_input("Enter your query:")

if st.button("Generate SQL"):
    if user_input:
        st.session_state.sql_query = generate_sql(user_input)
        st.session_state.executed = False
        st.session_state.result = None

# ─────────────────────────────────────────
# 🔥 Show Generated SQL
# ─────────────────────────────────────────
if st.session_state.sql_query:

    st.subheader("Generated SQL:")
    st.code(st.session_state.sql_query, language="sql")

    # 🔥 Show tables used
    tables = re.findall(r'FROM\s+(\w+)|JOIN\s+(\w+)', st.session_state.sql_query, re.IGNORECASE)
    table_list = list(set([t for pair in tables for t in pair if t]))
    if table_list:
        st.write("Tables used:", table_list)

    # ─────────────────────────────────────────
    # 🚨 Dangerous query flow
    # ─────────────────────────────────────────
    if is_dangerous(st.session_state.sql_query):

        st.warning("⚠️ This query will modify the database!")

        confirm = st.radio(
            "Do you want to execute this query?",
            ("No", "Yes"),
            index=0,  # ✅ always defaults to No on rerun
            key="confirm_radio"
        )

        if confirm == "Yes":
            if st.button("🚀 Execute Query"):
                if not st.session_state.executed:
                    st.session_state.result = run_query(st.session_state.sql_query)
                    st.session_state.executed = True
                    st.rerun()  # ✅ prevents double execution
        else:
            st.info("❌ Query cancelled")

    else:
        # ✅ Safe queries (SELECT) auto-execute once
        if not st.session_state.executed:
            st.session_state.result = run_query(st.session_state.sql_query)
            st.session_state.executed = True

# ─────────────────────────────────────────
# 🔥 Show Results
# ─────────────────────────────────────────
if st.session_state.result:

    st.subheader("Result:")
    result = st.session_state.result

    if "error" in result:
        st.error(result["error"])

    elif result.get("data"):
        df = pd.DataFrame(result["data"], columns=result["columns"])
        st.table(df)

    elif "message" in result:
        st.success(result["message"])

    else:
        st.warning("No results found")

# ─────────────────────────────────────────
# 🔥 Show updated table AFTER INSERT/UPDATE/DELETE
# ─────────────────────────────────────────
if st.session_state.executed and st.session_state.sql_query and is_dangerous(st.session_state.sql_query):

    st.subheader("🔄 Table After Modification:")

    # ✅ Dynamically extract the first table from the query instead of hardcoding
    tables = re.findall(r'FROM\s+(\w+)|JOIN\s+(\w+)', st.session_state.sql_query, re.IGNORECASE)
    table_list = [t for pair in tables for t in pair if t]

    if table_list:
        primary_table = table_list[0]
        updated = run_query(f"SELECT * FROM {primary_table}")

        if isinstance(updated, dict) and updated.get("data"):
            df = pd.DataFrame(updated["data"], columns=updated["columns"])
            st.table(df)
        else:
            st.warning(f"Could not fetch updated table: `{primary_table}`")
    else:
        st.warning("Could not determine which table to display.")