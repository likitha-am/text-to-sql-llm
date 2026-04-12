import ollama

def generate_sql(query):
    prompt = f"""
You are an expert SQL generator.

Database:
customers(id, name, age, city)

Rules:
- Only return SQL query
- No explanation
- Use only given table

Examples:
Q: Show all customers
A: SELECT * FROM customers;

Q: Find customers older than 30
A: SELECT * FROM customers WHERE age > 30;

Q: List customers from London
A: SELECT * FROM customers WHERE city = 'London';

Now convert:

Q: {query}
A:
"""

    response = ollama.chat(
        model='mistral',
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content'].strip()