from transformers import pipeline

generator = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_sql(query):
    prompt = f"""
You are a system that converts English to SQL.

Database schema:
Table customers(id, name, age, city)

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

    result = generator(prompt, max_new_tokens=50)
    sql = result[0]['generated_text'].strip()

    return sql