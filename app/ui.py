import streamlit as st
import pandas as pd

from llm.model import generate_sql
from database.db import (
    create_table,
    run_query,
    is_dangerous,
    extract_table_name
)

st.set_page_config(page_title="Text-to-SQL", layout="centered")

st.title("💬 Ask Your Database")

# (Optional demo setup)
create_table()

# 🔥 Session state
if "sql_query" not in st.session_state:
    st.session_state.sql_query = None

if "executed" not in st.session_state:
    st.session_state.executed = False

if "result" not in st.session_state:
    st.session_state.result = None

# Input
user_input = st.text_input("Enter your query:")

# Generate SQL
if st.button("Generate SQL"):
    if user_input:
        st.session_state.sql_query = generate_sql(user_input)
        st.session_state.executed = False
        st.session_state.result = None

# Show SQL
if st.session_state.sql_query:

    st.subheader("Generated SQL:")
    st.code(st.session_state.sql_query, language="sql")

    # Dangerous query handling
    if is_dangerous(st.session_state.sql_query):

        st.warning("⚠️ This query will modify the database!")

        confirm = st.radio(
            "Do you want to execute this query?",
            ("No", "Yes"),
            index=0,
            key="confirm_radio"
        )

        if confirm == "Yes":

            if st.button("🚀 Execute Query"):

                if not st.session_state.executed:
                    st.session_state.result = run_query(st.session_state.sql_query)
                    st.session_state.executed = True
                    st.rerun()

        else:
            st.info("❌ Query cancelled")

    else:
        if not st.session_state.executed:
            st.session_state.result = run_query(st.session_state.sql_query)
            st.session_state.executed = True

# Show result
if st.session_state.result:

    st.subheader("Result:")

    result = st.session_state.result

    if isinstance(result, dict):

        if "error" in result:
            st.error(result["error"])

        elif result.get("data"):
            df = pd.DataFrame(result["data"], columns=result["columns"])
            st.table(df)

        elif "message" in result:
            st.success(result["message"])

        else:
            st.warning("No results found")

    elif isinstance(result, list) and len(result) > 0:
        df = pd.DataFrame(result)
        st.table(df)

# 🔥 Show updated table dynamically
if (
    st.session_state.executed
    and st.session_state.sql_query
    and is_dangerous(st.session_state.sql_query)
):

    table_name = extract_table_name(st.session_state.sql_query)

    if table_name:
        st.subheader(f"🔄 Updated {table_name} Table:")

        updated = run_query(f"SELECT * FROM {table_name}")

        if isinstance(updated, dict) and updated.get("data"):
            df = pd.DataFrame(updated["data"], columns=updated["columns"])
            st.table(df)