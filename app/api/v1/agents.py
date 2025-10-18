"""
Agent API routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from app.mcp.protocol import MCPMessage, MCPResponse, mcp_handler
from app.agents.service import agent_service, Agent, AgentTask

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint for agents service"""
    return {"status": "healthy"}

class AgentCreate(BaseModel):
    name: str
    description: str
    model: str
    capabilities: List[str]

class AgentResponse(BaseModel):
    id: str
    name: str
    description: str
    model: str
    capabilities: List[str]
    status: str

class AgentTaskCreate(BaseModel):
    agent_id: str
    task_type: str
    parameters: Dict[str, Any]

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Any

# Agent endpoints
@router.post("/", response_model=AgentResponse)
async def create_agent(agent: AgentCreate):
    """
    Create a new agent with specified capabilities
    """
    new_agent = agent_service.create_agent(
        name=agent.name,
        description=agent.description,
        model=agent.model,
        capabilities=agent.capabilities
    )
    return AgentResponse(
        id=new_agent.id,
        name=new_agent.name,
        description=new_agent.description,
        model=new_agent.model,
        capabilities=new_agent.capabilities,
        status=new_agent.status
    )

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """
    Get agent by ID
    """
    agent = agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentResponse(
        id=agent.id,
        name=agent.name,
        description=agent.description,
        model=agent.model,
        capabilities=agent.capabilities,
        status=agent.status
    )

@router.get("/", response_model=List[AgentResponse])
async def list_agents():
    """
    List all agents
    """
    agents = agent_service.list_agents()
    return [
        AgentResponse(
            id=agent.id,
            name=agent.name,
            description=agent.description,
            model=agent.model,
            capabilities=agent.capabilities,
            status=agent.status
        )
        for agent in agents
    ]

@router.post("/tasks", response_model=TaskResponse)
async def create_task(task: AgentTaskCreate):
    """
    Create a task for an agent
    """
    agent_task = agent_service.create_task(
        agent_id=task.agent_id,
        task_type=task.task_type,
        parameters=task.parameters
    )
    if not agent_task:
        raise HTTPException(status_code=404, detail="Agent not found")
    return TaskResponse(
        task_id=agent_task.id,
        status=agent_task.status,
        result=agent_task.result
    )

@router.post("/tasks/{task_id}/execute")
async def execute_task(task_id: str):
    """
    Execute a task
    """
    task = await agent_service.execute_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task.id, "status": task.status, "result": task.result}

# MCP Protocol endpoints
@router.post("/mcp", response_model=MCPResponse)
async def handle_mcp_message(message: MCPMessage):
    """
    Handle an MCP (Model Coordination Protocol) message
    """
    response = await mcp_handler.handle_message(message)
    return response