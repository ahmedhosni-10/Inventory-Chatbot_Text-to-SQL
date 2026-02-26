from pydantic import BaseModel, Field
from typing import Literal, Optional, Any

class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class ChatRequest(BaseModel):
    session_id: str
    message: str
    context: Optional[dict[str, Any]] = None

class ChatResponse(BaseModel):
    natural_language_answer: str
    sql_query: str
    token_usage: TokenUsage
    latency_ms: int
    provider: Literal["openai", "azure"]
    model: str
    status: Literal["ok", "error"]
