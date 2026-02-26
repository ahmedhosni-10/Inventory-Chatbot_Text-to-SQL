import os
import json
from openai import OpenAI
from models import TokenUsage
from dotenv import load_dotenv

load_dotenv()

# Load original SQL Server DDL to provide accurate schema context
with open("schema.sql", "r") as f:
    SCHEMA_DDL = f.read()

# Initialize OpenAI Client (Compatible with Groq Cloud or generic OpenAI)
base_url = os.getenv("MODEL_BASE_URL")
client = OpenAI(
    api_key=os.getenv("MODEL_API_KEY"),
    base_url=base_url if base_url else None
)
MODEL_NAME = os.getenv("MODEL_NAME", "llama3-70b-8192")


def generate_sql_query(user_question: str) -> tuple[str, TokenUsage]:
    """
    Uses the LLM to convert a user question into a valid SQL query based on the database schema.
    """
    system_prompt = f"""You are a Text-to-SQL expert for an inventory management system.
Your job is to translate a user's natural language question into a valid SQL query.

Here is the exact DDL schema for the database:
{SCHEMA_DDL}

Key Instructions:
1. ONLY return the raw, valid SQL query text. Do not wrap it in markdown code blocks like ```sql ... ```. If you must use code blocks, output them, but I prefer just raw SQL.
2. The user wants queries that run against Microsoft SQL Server or standard ANSI SQL. The executed database locally will understand standard ANSI SQL like standard JOINs, WHERE clauses, and aggregations.
3. Assets are linked to Sites and Locations. Note the relationships constraints mapped in the DDL.
4. If a user asks "how many", use COUNT(*).
5. Always double check table and column names exactly as they appear in the schema.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0.0
    )

    sql_query = response.choices[0].message.content.strip()
    
    # Strip markdown code blocks if the LLM adds them despite instructions
    if sql_query.startswith("```sql"):
        sql_query = sql_query[6:]
    if sql_query.endswith("```"):
        sql_query = sql_query[:-3]
    
    sql_query = sql_query.strip()
    
    usage = response.usage
    token_usage = TokenUsage(
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens
    )
    
    return sql_query, token_usage


def generate_natural_answer(user_question: str, sql_query: str, query_results: list[dict], token_usage_so_far: TokenUsage) -> tuple[str, TokenUsage]:
    """
    Takes the execution results and translates it back into a conversational answer.
    """
    # Limit query result printing to avoid huge context windows for very large results
    results_str = json.dumps(query_results[:50], indent=2, default=str)
    if len(query_results) > 50:
        results_str += f"\\n...and {len(query_results) - 50} more rows."
        
    system_prompt = """You are an intelligent inventory assistant.
Your job is to read the results of a database query and answer the user's original question in a polite, concise, natural language format.
Do NOT reveal the raw JSON data to the user. Do format your response cleanly (use bullet points if listing multiple items).
"""

    user_prompt = f"""
User Question: {user_question}

SQL Query Used: 
{sql_query}

Query Results (JSON):
{results_str}

Please provide the final natural language answer.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content.strip()
    
    usage = response.usage
    final_token_usage = TokenUsage(
        prompt_tokens=token_usage_so_far.prompt_tokens + usage.prompt_tokens,
        completion_tokens=token_usage_so_far.completion_tokens + usage.completion_tokens,
        total_tokens=token_usage_so_far.total_tokens + usage.total_tokens
    )
    
    return answer, final_token_usage
