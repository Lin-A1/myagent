"""
Model Coordination Protocol (MCP) implementation
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

class MCPMessage(BaseModel):
    """
    MCP message format
    """
    id: str
    method: str
    params: Dict[str, Any]
    jsonrpc: str = "2.0"

class MCPResponse(BaseModel):
    """
    MCP response format
    """
    id: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    jsonrpc: str = "2.0"

class MCPProtocolHandler:
    """
    Handler for Model Coordination Protocol messages
    """
    
    def __init__(self):
        self.supported_methods = {
            "list_models": self.list_models,
            "get_model_info": self.get_model_info,
        }
    
    async def handle_message(self, message: MCPMessage) -> MCPResponse:
        """
        Handle an MCP message
        """
        try:
            if message.method not in self.supported_methods:
                return MCPResponse(
                    id=message.id,
                    error={
                        "code": -32601,
                        "message": f"Method '{message.method}' not found"
                    }
                )
            
            result = await self.supported_methods[message.method](message.params)
            return MCPResponse(id=message.id, result=result)
        except Exception as e:
            return MCPResponse(
                id=message.id,
                error={
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            )
    
    async def list_models(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List available models
        """
        return {
            "models": [
                {
                    "id": "llm-model-1",
                    "name": "LLM Model 1",
                    "description": "General purpose LLM model",
                    "capabilities": ["completion", "chat"]
                }
            ]
        }
    
    async def get_model_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about a specific model
        """
        model_id = params.get("model_id", "")
        return {
            "id": model_id,
            "name": f"LLM Model {model_id.split('-')[-1]}",
            "description": "LLM model information",
            "capabilities": ["completion", "chat"],
            "max_tokens": 4096,
            "temperature_range": [0.0, 1.0]
        }

# Global instance
mcp_handler = MCPProtocolHandler()