import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

def execute_query(sql_query: str) -> list[dict]:
    """
    Executes a raw SQL query and returns the results as a list of dictionaries.
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql_query))
        
        # Determine if it's a SELECT query
        if result.returns_rows:
            # Convert rows to dicts
            keys = result.keys()
            return [dict(zip(keys, row)) for row in result.fetchall()]
        else:
            # For UPDATE/INSERT/DELETE, return rows affected
            connection.commit()
            return [{"rows_affected": result.rowcount}]
