# 🤖 Inventory AI Chatbot (Text-to-SQL)

An intelligent AI service that translates natural language business questions into executable T-SQL queries and human-readable answers. 

![System Architecture](System%20Architecture%20Diagram.png)

[cite_start]This project implements a **"Present Query"** architecture, providing full transparency by returning the exact SQL code generated for every response[cite: 4].

## 🌟 Key Features
* [cite_start]**Natural Language to SQL:** Translates business questions like "How many assets by site?" into valid T-SQL [cite: 4, 49-51].
* [cite_start]**Transparency:** Returns the exact `sql_query` used to fetch data for every natural language answer.
* [cite_start]**Performance Metrics:** Tracks and returns `latency_ms` and detailed `token_usage` (prompt, completion, and total) [cite: 11-12].
* [cite_start]**Multi-Provider Support:** Fully compatible with **OpenAI**, **Azure**, and **Groq Cloud** (Llama 3.3 / DeepSeek) [cite: 13, 16-17].
* [cite_start]**Robust Mock Data:** Pre-initialized with realistic records for Assets, Sites, Vendors, and Orders to test all assignment scenarios [cite: 52-59].

## 🛠️ Tech Stack
* [cite_start]**Framework:** FastAPI (Python).
* [cite_start]**LLM Engine:** Groq Cloud (Llama-3.3-70b-versatile) or OpenAI/Azure[cite: 13, 19].
* [cite_start]**Database:** SQLite (Configured with SQL Server DDL for enterprise compatibility) .
* [cite_start]**Environment:** Python-dotenv for secure configuration[cite: 18].

## 📂 Project Structure
```text
├── .env                # API Keys & Configuration (Excluded from Git)
[cite_start]├── main.py             # FastAPI entry point & POST/api/chat route 
├── llm.py              # Logic for AI prompt engineering and SQL generation
├── database.py         # Database connection and T-SQL execution logic
[cite_start]├── init_db.py          # Script to build schema and seed mock records 
[cite_start]├── models.py           # Pydantic schemas for request/response validation [cite: 6-15]
└── requirements.txt    # Project dependencies


