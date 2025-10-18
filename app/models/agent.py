"""
Agent model for storing agent configurations
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY
from app.modules.database.database import Base
from datetime import datetime

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    model = Column(String, nullable=False)
    capabilities = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)