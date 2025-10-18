"""
API tests for the LLM Agent Platform
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_llm_health():
    """Test the LLM health endpoint"""
    response = client.get("/api/v1/llm/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_llm_models():
    """Test the LLM models endpoint"""
    response = client.get("/api/v1/llm/models")
    assert response.status_code == 200
    assert "data" in response.json()

def test_llm_completions():
    """Test the LLM completions endpoint"""
    response = client.post(
        "/api/v1/llm/completions",
        json={
            "model": "llm-model-1",
            "prompt": "Say hello",
            "temperature": 0.7,
            "max_tokens": 100
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "choices" in data
    assert len(data["choices"]) > 0

def test_llm_chat_completions():
    """Test the LLM chat completions endpoint"""
    response = client.post(
        "/api/v1/llm/chat/completions",
        json={
            "model": "llm-model-1",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "choices" in data
    assert len(data["choices"]) > 0

def test_auth_health():
    """Test the auth health endpoint"""
    response = client.get("/api/v1/auth/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_agents_health():
    """Test the agents health endpoint"""
    response = client.get("/api/v1/agents/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

if __name__ == "__main__":
    pytest.main([__file__])