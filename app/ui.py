import streamlit as st
from llm.model import generate_sql
from database.db import create_table, run_query

st.set_page_config(page_title="Text-to-SQL", layout="centered")

st.title("💬 Ask Your Database")

create_table()

user_input = st.text_input("Enter your query:")

if st.button("Generate SQL"):

    if user_input:
        sql_query = generate_sql(user_input)

        st.subheader("Generated SQL:")
        st.code(sql_query, language="sql")

        result = run_query(sql_query)

        st.subheader("Result:")
        st.write(result)