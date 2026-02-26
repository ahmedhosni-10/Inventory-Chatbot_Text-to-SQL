import time
import os
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from models import ChatRequest, ChatResponse, TokenUsage
from llm import generate_sql_query, generate_natural_answer
from database import execute_query
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Inventory AI Chat API", version="1.0.0")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    
    try:
        # Step 1: Generate SQL from natural language
        try:
            sql_query, initial_tokens = generate_sql_query(request.message)
        except Exception as e:
            raise Exception(f"Failed to generate SQL: {str(e)}")

        # Step 2: Execute the query
        try:
            results = execute_query(sql_query)
        except Exception as e:
            # Note: We return status \"error\" but still include the generated SQL
            # per instructions returning a structured JSON response on errors too.
            latency = int((time.time() - start_time) * 1000)
            return ChatResponse(
                natural_language_answer=f"Error executing database query: {str(e)}",
                sql_query=sql_query,
                token_usage=initial_tokens,
                latency_ms=latency,
                provider=os.getenv("PROVIDER", "openai"),
                model=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
                status="error"
            )

        # Step 3: Generate Natural Language Answer
        try:
            answer, final_tokens = generate_natural_answer(
                user_question=request.message,
                sql_query=sql_query,
                query_results=results,
                token_usage_so_far=initial_tokens
            )
        except Exception as e:
            raise Exception(f"Failed to generate answer: {str(e)}")
            
        latency = int((time.time() - start_time) * 1000)

        # Step 4: Return formatted JSON
        return ChatResponse(
            natural_language_answer=answer,
            sql_query=sql_query,
            token_usage=final_tokens,
            latency_ms=latency,
            provider=os.getenv("PROVIDER", "openai"),
            model=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
            status="ok"
        )

    except Exception as e:
        latency = int((time.time() - start_time) * 1000)
        return ChatResponse(
            natural_language_answer=f"An unexpected error occurred: {str(e)}",
            sql_query="",
            token_usage=TokenUsage(),
            latency_ms=latency,
            provider=os.getenv("PROVIDER", "openai"),
            model=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
            status="error"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
