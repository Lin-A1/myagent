"""
Agent tests for the LLM Agent Platform
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.modules.agents.agent_service import agent_service

client = TestClient(app)

def test_agent_creation():
    """Test agent creation"""
    # Test creating an agent
    agent = agent_service.create_agent(
        name="Test Agent",
        description="A test agent",
        model="llm-model-1",
        capabilities=["completion", "chat"]
    )
    
    assert agent is not None
    assert agent.name == "Test Agent"
    assert agent.description == "A test agent"
    assert agent.model == "llm-model-1"
    assert agent.capabilities == ["completion", "chat"]

def test_agent_retrieval():
    """Test agent retrieval"""
    # Create an agent first
    agent = agent_service.create_agent(
        name="Test Agent 2",
        description="Another test agent",
        model="llm-model-2",
        capabilities=["completion"]
    )
    
    # Retrieve the agent
    retrieved_agent = agent_service.get_agent(agent.id)
    
    assert retrieved_agent is not None
    assert retrieved_agent.id == agent.id
    assert retrieved_agent.name == "Test Agent 2"

def test_agent_listing():
    """Test listing agents"""
    # Get all agents
    agents = agent_service.list_agents()
    
    assert isinstance(agents, list)
    # Should have at least the agents we created in previous tests

def test_agent_task_creation():
    """Test creating agent tasks"""
    # Create an agent first
    agent = agent_service.create_agent(
        name="Task Agent",
        description="Agent for testing tasks",
        model="llm-model-1",
        capabilities=["completion"]
    )
    
    # Create a task for the agent
    task = agent_service.create_task(
        agent_id=agent.id,
        task_type="completion",
        parameters={"prompt": "Hello, world!"}
    )
    
    assert task is not None
    assert task.agent_id == agent.id
    assert task.task_type == "completion"
    assert task.parameters == {"prompt": "Hello, world!"}

def test_agent_api_endpoints():
    """Test agent API endpoints"""
    # Test agent health endpoint
    response = client.get("/api/v1/agents/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

if __name__ == "__main__":
    pytest.main([__file__])