from rag.vector_store import search_schema
from database.db import get_relationships


def build_schema_context(user_query):
    results = search_schema(user_query, top_k=10)
    relationships = get_relationships()

    schema_dict = {}

    for item in results:
        table = item["table"]
        column = item["column"]

        if table not in schema_dict:
            schema_dict[table] = set()

        schema_dict[table].add(column)

    schema = ""

    # 🔥 Add tables + columns
    for table, columns in schema_dict.items():
        schema += f"{table}({', '.join(columns)})\n"

    # ✅ Make JOIN instructions crystal clear for the LLM
    if relationships:
        schema += "\nRelationships (YOU MUST USE JOIN FOR THESE):\n"
        for rel in relationships:
            schema += (
                f"- {rel['table']} JOIN {rel['to_table']} "
                f"ON {rel['table']}.{rel['from']} = {rel['to_table']}.{rel['to']}\n"
            )

    return schema