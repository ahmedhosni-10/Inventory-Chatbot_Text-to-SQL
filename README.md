# 🤖 Inventory AI Chatbot (Text-to-SQL)

An intelligent AI service that translates natural language business questions into executable T-SQL queries and human-readable answers. Designed for inventory management transparency using the **"Present Query"** architecture.
![System Architecture](System%20Architecture%20Diagram.png)


## 🌟 Key Features
* **Natural Language to SQL:** Translates questions like "How many assets by site?" into valid T-SQL.
* **Transparency:** Returns the exact `sql_query` executed by the system for every answer.
* **Performance Tracking:** Real-time monitoring of `latency_ms` and `token_usage` (prompt, completion, and total).
* **Robust Mock Data:** Pre-initialized with realistic records for Assets, Sites, Vendors, and Orders to test all assignment scenarios.
* **Multi-Provider Support:** Compatible with **OpenAI**, **Azure**, and **Groq Cloud** (Llama 3.3 / DeepSeek).

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python).
* **LLM Engine:** Groq Cloud (Llama-3.3-70b-versatile) / OpenAI.
* **Database:** SQLite (Configured with SQL Server DDL for compatibility).
* **Environment:** Python-dotenv for secure configuration.

## 📂 Project Structure
```text
├── .env                # API Keys & Configuration (Hidden)
├── main.py             # FastAPI entry point & API routes
├── llm.py              # LLM Integration logic (Groq/OpenAI)
├── database.py         # SQL execution & connection management
├── init_db.py          # Schema creation & Mock data seeding
├── models.py           # Pydantic models for JSON validation
└── requirements.txt    # Python dependencies


