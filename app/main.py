from llm.model import generate_sql

while True:
    user_input = input("Ask your query: ")

    if user_input.lower() == "exit":
        break

    sql_query = generate_sql(user_input)

    print("\nGenerated SQL:")
    print(sql_query)
    print("-" * 50)
