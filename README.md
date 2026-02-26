
# 🤖 Inventory AI Chatbot (Text-to-SQL)

An intelligent AI service that translates natural language business questions into executable T-SQL queries and human-readable answers. Designed for inventory management transparency using the **"Present Query"** architecture.



## 🌟 Key Features
* [cite_start]**Natural Language to SQL:** Translates questions like "How many assets by site?" into valid T-SQL [cite: 4, 49-51].
* [cite_start]**Transparency:** Returns the exact `sql_query` executed by the system for every answer[cite: 10, 45].
* [cite_start]**Performance Tracking:** Real-time monitoring of `latency_ms` and `token_usage` (prompt, completion, and total) [cite: 11-12].
* [cite_start]**Robust Mock Data:** Pre-initialized with realistic records for Assets, Sites, Vendors, and Orders to test all assignment scenarios [cite: 52-59].
* [cite_start]**Multi-Provider Support:** Compatible with **OpenAI**, **Azure**, and **Groq Cloud** (Llama 3.3 / DeepSeek)[cite: 13, 17].

## 🛠️ Tech Stack
* [cite_start]**Framework:** FastAPI (Python).
* **LLM Engine:** Groq Cloud (Llama-3.3-70b-versatile) / OpenAI.
* [cite_start]**Database:** SQLite (Configured with SQL Server DDL for compatibility) [cite: 20-43].
* [cite_start]**Environment:** Python-dotenv for secure configuration[cite: 18].

## 📂 Project Structure
```text
├── .env                # API Keys & Configuration (Hidden)
├── main.py             # FastAPI entry point & API routes
├── llm.py              # LLM Integration logic (Groq/OpenAI)
├── database.py         # SQL execution & connection management
├── init_db.py          # Schema creation & Mock data seeding
├── models.py           # Pydantic models for JSON validation
└── requirements.txt    # Python dependencies
