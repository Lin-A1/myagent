"""
MCP protocol tests for the LLM Agent Platform
"""
import pytest
from app.modules.mcp.mcp_protocol import MCPMessage, MCPResponse, mcp_handler

def test_mcp_message_creation():
    """Test MCP message creation"""
    message = MCPMessage(
        id="test-123",
        method="test_method",
        params={"key": "value"}
    )
    
    assert message.id == "test-123"
    assert message.method == "test_method"
    assert message.params == {"key": "value"}
    assert message.jsonrpc == "2.0"

def test_mcp_response_creation():
    """Test MCP response creation"""
    response = MCPResponse(
        id="test-123",
        result={"data": "test"}
    )
    
    assert response.id == "test-123"
    assert response.result == {"data": "test"}
    assert response.error is None
    assert response.jsonrpc == "2.0"

def test_mcp_error_response():
    """Test MCP error response creation"""
    response = MCPResponse(
        id="test-123",
        error={"code": -32601, "message": "Method not found"}
    )
    
    assert response.id == "test-123"
    assert response.result is None
    assert response.error == {"code": -32601, "message": "Method not found"}
    assert response.jsonrpc == "2.0"

def test_mcp_handler_list_models():
    """Test MCP handler list models method"""
    import asyncio
    
    message = MCPMessage(
        id="test-123",
        method="list_models",
        params={}
    )
    
    # Run the async method
    response = asyncio.run(mcp_handler.handle_message(message))
    
    assert isinstance(response, MCPResponse)
    assert response.id == "test-123"
    assert response.result is not None
    assert "models" in response.result

def test_mcp_handler_unknown_method():
    """Test MCP handler with unknown method"""
    import asyncio
    
    message = MCPMessage(
        id="test-123",
        method="unknown_method",
        params={}
    )
    
    # Run the async method
    response = asyncio.run(mcp_handler.handle_message(message))
    
    assert isinstance(response, MCPResponse)
    assert response.id == "test-123"
    assert response.error is not None
    assert response.error["code"] == -32601

if __name__ == "__main__":
    pytest.main([__file__])