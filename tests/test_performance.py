"""
Performance tests for the LLM Agent Platform
"""
import time
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_response_time():
    """Test API response time"""
    start_time = time.time()
    
    # Make a simple API call
    response = client.get("/health")
    
    end_time = time.time()
    response_time = end_time - start_time
    
    assert response.status_code == 200
    # Response should be under 1 second
    assert response_time < 1.0

def test_concurrent_requests():
    """Test concurrent requests performance"""
    import threading
    
    def make_request():
        response = client.get("/health")
        assert response.status_code == 200
    
    # Make 10 concurrent requests
    threads = []
    start_time = time.time()
    
    for i in range(10):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # All 10 requests should complete within 2 seconds
    assert total_time < 2.0

def test_llm_service_performance():
    """Test LLM service performance"""
    from app.modules.core.llm_service import llm_service
    
    start_time = time.time()
    
    # Test completion creation
    import asyncio
    result = asyncio.run(llm_service.create_completion(
        model="test-model",
        prompt="Hello, world!"
    ))
    
    end_time = time.time()
    response_time = end_time - start_time
    
    assert result is not None
    # Response should be under 2 seconds
    assert response_time < 2.0

def test_cache_performance():
    """Test cache performance"""
    from app.modules.database.redis_client import redis_client
    
    # Skip if Redis is not available
    if not redis_client.is_connected:
        pytest.skip("Redis server not available")
    
    test_key = "performance_test_key"
    test_value = "performance_test_value"
    
    # Set a value
    start_time = time.time()
    redis_client.set(test_key, test_value, expire=10)
    set_time = time.time() - start_time
    
    # Get the value (should be fast due to cache)
    start_time = time.time()
    retrieved_value = redis_client.get(test_key)
    get_time = time.time() - start_time
    
    # Delete the value
    redis_client.delete(test_key)
    
    assert retrieved_value == test_value
    # Both operations should be fast
    assert set_time < 1.0
    assert get_time < 0.1  # Cache retrieval should be very fast

if __name__ == "__main__":
    pytest.main([__file__])