"""
Integration tests for the LLM Agent Platform
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.modules.agents.agent_service import agent_service
from app.modules.mcp.mcp_protocol import MCPMessage

client = TestClient(app)

def test_full_llm_workflow():
    """Test full LLM workflow from API to service"""
    # Test LLM models endpoint
    response = client.get("/api/v1/llm/models")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    
    # Test completion endpoint
    response = client.post(
        "/api/v1/llm/completions",
        json={
            "model": "llm-model-1",
            "prompt": "Hello, world!",
            "temperature": 0.7,
            "max_tokens": 100
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "choices" in data

def test_full_agent_workflow():
    """Test full agent workflow"""
    # Create an agent via API
    response = client.post(
        "/api/v1/agents/",
        json={
            "name": "Integration Test Agent",
            "description": "Agent for integration testing",
            "model": "llm-model-1",
            "capabilities": ["completion", "chat"]
        }
    )
    assert response.status_code == 200
    agent_data = response.json()
    agent_id = agent_data["id"]
    
    # Create a task for the agent
    response = client.post(
        "/api/v1/agents/tasks",
        json={
            "agent_id": agent_id,
            "task_type": "completion",
            "parameters": {"prompt": "Hello from integration test!"}
        }
    )
    assert response.status_code == 200
    task_data = response.json()
    task_id = task_data["task_id"]
    
    # Execute the task
    response = client.post(f"/api/v1/agents/tasks/{task_id}/execute")
    assert response.status_code == 200

def test_mcp_integration():
    """Test MCP protocol integration"""
    import asyncio
    
    # Test MCP message handling through API
    response = client.post(
        "/api/v1/agents/mcp",
        json={
            "id": "integration-test-123",
            "method": "list_models",
            "params": {},
            "jsonrpc": "2.0"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "integration-test-123"
    assert "result" in data

def test_middleware_integration():
    """Test middleware integration"""
    # Test that middleware is properly applied
    response = client.get("/")
    assert response.status_code == 200
    
    # Test authentication middleware (this should fail without auth)
    response = client.get("/api/v1/auth/users/me")
    assert response.status_code == 401  # Unauthorized

def test_database_integration():
    """Test database integration"""
    # Test that database models can be imported
    from app.modules.database.database import Base
    from app.models.user import User
    from app.models.agent import Agent
    from app.models.llm import LLMModel, LLMUsage
    
    # Test that models inherit from Base
    assert issubclass(User, Base)
    assert issubclass(Agent, Base)
    assert issubclass(LLMModel, Base)
    assert issubclass(LLMUsage, Base)

def test_end_to_end_workflow():
    """Test end-to-end workflow"""
    # 1. Create an agent
    response = client.post(
        "/api/v1/agents/",
        json={
            "name": "End-to-End Test Agent",
            "description": "Agent for end-to-end testing",
            "model": "llm-model-1",
            "capabilities": ["completion"]
        }
    )
    assert response.status_code == 200
    agent_data = response.json()
    agent_id = agent_data["id"]
    
    # 2. List available models
    response = client.get("/api/v1/llm/models")
    assert response.status_code == 200
    
    # 3. Create a completion
    response = client.post(
        "/api/v1/llm/completions",
        json={
            "model": "llm-model-1",
            "prompt": "End-to-end test completion",
            "temperature": 0.7,
            "max_tokens": 50
        }
    )
    assert response.status_code == 200
    
    # 4. Create and execute an agent task
    response = client.post(
        "/api/v1/agents/tasks",
        json={
            "agent_id": agent_id,
            "task_type": "completion",
            "parameters": {"prompt": "Agent task end-to-end test"}
        }
    )
    assert response.status_code == 200
    task_data = response.json()
    task_id = task_data["task_id"]
    
    response = client.post(f"/api/v1/agents/tasks/{task_id}/execute")
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__])