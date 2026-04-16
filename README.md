# 🧠 AskSQL — Natural Language to SQL with RAG (and a lot of debugging)

## Overview

This project is a local, end-to-end **Text-to-SQL system** that lets you ask questions in plain English and get actual SQL queries and results from a database.

In simple terms:
You type something like
“show customer names with their order amounts”
and the system figures out the SQL, runs it, and gives you the result.

No SQL knowledge required.
(But after building this, you’ll accidentally learn SQL anyway.)

---

## Why this exists

Most Text-to-SQL demos look impressive until you try anything slightly real.

They:

* Break when multiple tables are involved
* Guess random columns
* Forget to add JOINs
* Or confidently return nonsense

So this project tries to fix that by building things properly:

* Adding RAG (Retrieval-Augmented Generation)
* Making the system schema-aware
* Handling multi-table queries
* Preventing completely broken SQL

---

## What this system does

* Converts natural language → SQL
* Executes SQL on a real SQLite database
* Supports dynamic CSV uploads (turns them into tables)
* Uses RAG to understand schema (tables + columns)
* Uses vector embeddings for semantic matching
* Attempts JOINs when multiple tables are involved
* Shows results in a clean UI

---

## Tech Stack

* **Python** (backend logic)
* **Streamlit** (UI)
* **SQLite** (database)
* **Ollama (Mistral)** (LLM, runs locally)
* **Sentence Transformers** (embeddings)
* **FAISS** (vector search)

Everything runs locally. No API keys. No cloud dependency.

---

## How it works (pipeline)

1. User enters a query
2. System retrieves relevant schema using embeddings
3. Expands context using table relationships
4. Sends structured prompt to LLM
5. LLM generates SQL
6. SQL is executed on SQLite
7. Results are displayed

---

## Key Features

### 1. Natural Language → SQL

No rigid input. You can ask casually:

* “products above 300”
* “customers with high orders”
* “show names and amounts”
Sometimes it works perfectly. Sometimes it teaches you humility.
---

### 2. RAG (Retrieval-Augmented Generation)

Instead of dumping the entire database into the model, it:
* Picks relevant tables
* Picks relevant columns
* Sends only useful context
This reduces confusion and improves accuracy.
---
### 3. Vector-Based Retrieval

Uses embeddings to understand meaning, not just keywords.

Example:

* “cost” → “price”
* “items” → “product”

This is where things start feeling intelligent.

---

### 4. Multi-table + JOIN support

The system:

* Detects multiple tables
* Uses relationships
* Attempts JOINs

Not perfect, but definitely not dumb.

---

### 5. CSV Upload → Instant Database

Upload any CSV:

* It becomes a table
* Schema is detected automatically
* You can query it immediately

No manual setup required.

---

### 6. Safe Execution (basic)

Detects potentially dangerous queries like:

* DELETE
* DROP
* UPDATE

And asks for confirmation.

Because trusting an LLM blindly is… not a great idea.

---

## How to run

1. Install dependencies:

```
pip install streamlit pandas sentence-transformers faiss-cpu
```

2. Start Ollama:

```
ollama serve
ollama pull mistral
```

3. Run the app:

```
streamlit run app/ui.py
```

---

## How to use

1. Upload CSV files (optional but recommended)
2. Type a natural language query
3. Click “Generate SQL”
4. See:

   * Generated SQL
   * Tables used
   * Result

---

## Example Queries

* show all customers
* products with price greater than 300
* show customer names with their order amounts
* total order amount per customer

---

## Known Limitations

* JOINs are not always perfect
* Complex queries may fail
* LLM may occasionally hallucinate
* “expensive” doesn’t magically mean `> 500` (yet)

Basically, it’s smart — but not psychic.

---

## What makes this project interesting

This is not just:
“call LLM → print result”

It includes:

* Pipeline design
* Retrieval system (RAG)
* Vector similarity
* Schema awareness
* Debugging real-world issues

It’s closer to how real AI systems are built.
---
## Future Improvements

* Better JOIN inference
* Query validation and auto-correction
* Support for PostgreSQL/MySQL
* Role-based access
* Smarter reasoning (handling vague terms like “cheap”, “expensive”)
---
## Final Note

This project started simple and slowly became something much bigger.
At some point, it stopped being “just a project”
and became:
“why is this SQL wrong and why is the model acting like this”
Which is honestly where real learning happens.
