"""
Middleware tests for the LLM Agent Platform
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_middleware_logging():
    """Test middleware logging functionality"""
    response = client.get("/")
    assert response.status_code == 200

def test_middleware_rate_limiting():
    """Test middleware rate limiting functionality"""
    # Make multiple requests to test rate limiting
    for i in range(5):
        response = client.get("/")
        assert response.status_code == 200

def test_middleware_caching():
    """Test middleware caching functionality"""
    # Make a request that should be cached
    response1 = client.get("/api/v1/llm/models")
    assert response1.status_code == 200
    
    # Make the same request again - should be served from cache
    response2 = client.get("/api/v1/llm/models")
    assert response2.status_code == 200
    
    # Responses should be identical
    assert response1.json() == response2.json()

if __name__ == "__main__":
    pytest.main([__file__])