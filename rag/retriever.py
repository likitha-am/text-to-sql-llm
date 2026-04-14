from database.db import get_all_tables, get_table_schema

def retrieve_relevant_tables(user_query):
    tables = get_all_tables()

    query = user_query.lower()
    relevant_tables = []

    for table in tables:
        if table.lower() in query:
            relevant_tables.append(table)

    # 🔥 fallback → if nothing matches, return all tables
    if not relevant_tables:
        return tables

    return relevant_tables


def build_schema_context(user_query):
    tables = retrieve_relevant_tables(user_query)

    schema = ""

    for table in tables:
        schema += get_table_schema(table) + "\n"

    return schema