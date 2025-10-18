"""
Application startup and shutdown handlers
"""
from app.database.connection import engine, Base
from app.core.llm_service import llm_service

async def startup_event():
    """
    Application startup event handler
    """
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Application startup completed")

async def shutdown_event():
    """
    Application shutdown event handler
    """
    # Close LLM service
    await llm_service.close()
    
    print("Application shutdown completed")