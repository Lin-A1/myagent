"""
API routes for the LLM Agent Platform
"""
from fastapi import APIRouter

from app.api.v1 import llm, auth, agents

router = APIRouter()

# Include API version 1 routes
router.include_router(llm.router, prefix="/llm", tags=["llm"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(agents.router, prefix="/agents", tags=["agents"])

# Health check endpoint
@router.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}