"""
LLM API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.core.llm_service import llm_service

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint for LLM service"""
    return {"status": "healthy"}

class CompletionRequest(BaseModel):
    model: str
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 100
    stop: Optional[List[str]] = None
    stream: bool = False

class CompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list
    usage: dict

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 100
    stop: Optional[List[str]] = None
    stream: bool = False

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

@router.post("/completions", response_model=CompletionResponse)
async def create_completion(request: CompletionRequest):
    """
    Create a completion for the provided prompt and parameters.
    Compatible with OpenAI API.
    """
    # Call the LLM service to create a completion
    result = await llm_service.create_completion(
        model=request.model,
        prompt=request.prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    return result

@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    """
    Create a chat completion for the provided messages and parameters.
    Compatible with OpenAI API.
    """
    # Convert messages to the format expected by the LLM service
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    # Call the LLM service to create a chat completion
    result = await llm_service.create_chat_completion(
        model=request.model,
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    return result

@router.get("/models")
async def list_models():
    """
    List available models.
    Compatible with OpenAI API.
    """
    # Call the LLM service to list models
    result = await llm_service.list_models()
    return result