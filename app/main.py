from llm.model import generate_sql
from database.db import create_table, run_query

create_table()

while True:
    user_input = input("Ask your query: ")

    if user_input.lower() == "exit":
        break

    sql_query = generate_sql(user_input)

    print("\nGenerated SQL:")
    print(sql_query)

    result = run_query(sql_query)

    print("\nResult:")
    print(result)

    print("-" * 50)