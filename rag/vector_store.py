from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import sqlite3

from database.db import get_all_tables

model = SentenceTransformer('all-MiniLM-L6-v2')


def get_columns(table_name):
    conn = sqlite3.connect("database/sample.db")
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    conn.close()

    return [col[1] for col in columns]


def build_vector_store():
    tables = get_all_tables()

    texts = []
    metadata = []

    for table in tables:
        columns = get_columns(table)

        for col in columns:
            texts.append(f"{table} {col}")
            metadata.append({"table": table, "column": col})

    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return index, metadata, texts


def search_schema(query, top_k=10):
    index, metadata, texts = build_vector_store()

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)

    # ✅ Collect all tables that were matched
    matched_tables = set()
    for idx in indices[0]:
        matched_tables.add(metadata[idx]["table"])

    # ✅ Return ALL columns for every matched table — not just top_k hits
    # This ensures JOINs have full schema context
    results = []
    for item in metadata:
        if item["table"] in matched_tables:
            results.append(item)

    return results