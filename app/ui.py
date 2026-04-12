import streamlit as st
from llm.model import generate_sql
from database.db import create_table, run_query
import pandas as pd

st.set_page_config(page_title="Text-to-SQL", layout="centered")

st.title(" Ask Your Database")

create_table()

user_input = st.text_input("Enter your query:")

if st.button("Generate SQL"):

    if user_input:
        sql_query = generate_sql(user_input)

        st.subheader("Generated SQL:")
        st.code(sql_query, language="sql")

        result = run_query(sql_query)
        

        st.subheader("Result:")

        # Case 1: New dict format
        if isinstance(result, dict):

            if "error" in result:
                st.error(result["error"])

            elif result.get("data"):
                df = pd.DataFrame(result["data"], columns=result["columns"])
                st.table(df)

            else:
                st.warning("No results found")

        # Case 2: Old list format (THIS is your current case)
        elif isinstance(result, list) and len(result) > 0:
            df = pd.DataFrame(result)
            df.columns = ["ID", "Name", "Age", "City"]  # temporary
            st.table(df)

        else:
            st.warning("No results found")