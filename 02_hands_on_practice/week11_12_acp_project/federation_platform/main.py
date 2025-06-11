"""
ACP Federation Platform - Main FastAPI Server
Agent Communication Protocol implementation for federated learning
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import asyncio
import uvicorn
import logging
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import uuid

from api.agents import router as agents_router
from api.discovery import router as discovery_router
from api.federation import router as federation_router
from core.registry import AgentRegistry
from core.executor import ExecutionEngine
from core.knowledge_store import KnowledgeStore
from models.agent import Agent, AgentDetail
from models.message import Message, MessagePart
from models.run import Run, RunStatus

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
agent_registry: Optional[AgentRegistry] = None
execution_engine: Optional[ExecutionEngine] = None
knowledge_store: Optional[KnowledgeStore] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting ACP Federation Platform...")
    
    global agent_registry, execution_engine, knowledge_store
    
    # Initialize core components
    agent_registry = AgentRegistry()
    execution_engine = ExecutionEngine()
    knowledge_store = KnowledgeStore()
    
    # Initialize database connections
    await agent_registry.initialize()
    await execution_engine.initialize()
    await knowledge_store.initialize()
    
    # Register default agents
    await register_default_agents()
    
    logger.info("ACP Federation Platform started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down ACP Federation Platform...")
    
    if knowledge_store:
        await knowledge_store.close()
    if execution_engine:
        await execution_engine.close()
    if agent_registry:
        await agent_registry.close()
    
    logger.info("ACP Federation Platform shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="ACP Federation Platform",
    description="Agent Communication Protocol implementation for federated learning",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents_router, prefix="/agents", tags=["agents"])
app.include_router(discovery_router, prefix="/discovery", tags=["discovery"])
app.include_router(federation_router, prefix="/federation", tags=["federation"])

@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "name": "ACP Federation Platform",
        "version": "1.0.0",
        "description": "Agent Communication Protocol implementation for federated learning",
        "endpoints": {
            "agents": "/agents",
            "discovery": "/discovery",
            "federation": "/federation",
            "health": "/health"
        },
        "timestamp": datetime.utcnow().isoformat(),
        "active_agents": await agent_registry.count() if agent_registry else 0
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # Check registry health
    if agent_registry:
        try:
            await agent_registry.health_check()
            health_status["components"]["registry"] = "healthy"
        except Exception as e:
            health_status["components"]["registry"] = f"unhealthy: {str(e)}"
            health_status["status"] = "degraded"
    
    # Check execution engine health
    if execution_engine:
        try:
            await execution_engine.health_check()
            health_status["components"]["executor"] = "healthy"
        except Exception as e:
            health_status["components"]["executor"] = f"unhealthy: {str(e)}"
            health_status["status"] = "degraded"
    
    # Check knowledge store health
    if knowledge_store:
        try:
            await knowledge_store.health_check()
            health_status["components"]["knowledge_store"] = "healthy"
        except Exception as e:
            health_status["components"]["knowledge_store"] = f"unhealthy: {str(e)}"
            health_status["status"] = "degraded"
    
    return health_status

@app.get("/metrics")
async def metrics():
    """Platform metrics endpoint"""
    metrics_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "agents": {
            "total": await agent_registry.count() if agent_registry else 0,
            "active": await agent_registry.count_active() if agent_registry else 0,
            "by_framework": await agent_registry.get_framework_stats() if agent_registry else {}
        },
        "runs": {
            "total": await execution_engine.get_total_runs() if execution_engine else 0,
            "active": await execution_engine.get_active_runs() if execution_engine else 0,
            "completed": await execution_engine.get_completed_runs() if execution_engine else 0,
            "failed": await execution_engine.get_failed_runs() if execution_engine else 0
        },
        "knowledge": {
            "total_entries": await knowledge_store.count_entries() if knowledge_store else 0,
            "total_size_mb": await knowledge_store.get_size_mb() if knowledge_store else 0,
            "federations_active": await knowledge_store.count_active_federations() if knowledge_store else 0
        }
    }
    
    return metrics_data

# ACP Standard API Endpoints

@app.get("/agents/{agent_id}", response_model=AgentDetail)
async def get_agent_detail(agent_id: str):
    """Get agent details (ACP standard endpoint)"""
    if not agent_registry:
        raise HTTPException(status_code=500, detail="Agent registry not initialized")
    
    agent = await agent_registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    return agent

@app.post("/agents/{agent_id}/runs")
async def create_agent_run(
    agent_id: str,
    request_data: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Create and execute agent run (ACP standard endpoint)"""
    if not agent_registry or not execution_engine:
        raise HTTPException(status_code=500, detail="Platform not initialized")
    
    # Validate agent exists
    agent = await agent_registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    # Create run
    run_id = str(uuid.uuid4())
    
    try:
        # Parse input messages
        input_messages = []
        if "input" in request_data:
            for msg_data in request_data["input"]:
                parts = []
                for part_data in msg_data.get("parts", []):
                    part = MessagePart(
                        content=part_data["content"],
                        content_type=part_data.get("content_type", "text/plain")
                    )
                    parts.append(part)
                
                message = Message(parts=parts)
                input_messages.append(message)
        
        # Create run record
        run = Run(
            id=run_id,
            agent_id=agent_id,
            status=RunStatus.QUEUED,
            input_messages=input_messages,
            created_at=datetime.utcnow()
        )
        
        # Queue execution
        background_tasks.add_task(
            execution_engine.execute_run,
            run,
            agent
        )
        
        return {
            "run_id": run_id,
            "status": "queued",
            "agent_id": agent_id,
            "created_at": run.created_at.isoformat(),
            "stream_url": f"/agents/{agent_id}/runs/{run_id}/stream"
        }
        
    except Exception as e:
        logger.error(f"Failed to create run for agent {agent_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to create run: {str(e)}")

@app.get("/agents/{agent_id}/runs/{run_id}")
async def get_run_status(agent_id: str, run_id: str):
    """Get run status and results (ACP standard endpoint)"""
    if not execution_engine:
        raise HTTPException(status_code=500, detail="Execution engine not initialized")
    
    run = await execution_engine.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    
    if run.agent_id != agent_id:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found for agent {agent_id}")
    
    response = {
        "run_id": run_id,
        "status": run.status.value,
        "agent_id": agent_id,
        "created_at": run.created_at.isoformat(),
        "updated_at": run.updated_at.isoformat() if run.updated_at else None,
    }
    
    if run.output_messages:
        response["output"] = [
            {
                "parts": [
                    {
                        "content": part.content,
                        "content_type": part.content_type
                    }
                    for part in message.parts
                ]
            }
            for message in run.output_messages
        ]
    
    if run.error:
        response["error"] = run.error
    
    return response

@app.get("/agents/{agent_id}/runs/{run_id}/stream")
async def stream_run_results(agent_id: str, run_id: str):
    """Stream run results in real-time (ACP extension)"""
    if not execution_engine:
        raise HTTPException(status_code=500, detail="Execution engine not initialized")
    
    async def event_stream():
        """Server-Sent Events stream for run results"""
        try:
            async for update in execution_engine.stream_run_updates(run_id):
                yield f"data: {json.dumps(update)}\n\n"
        except Exception as e:
            error_update = {
                "type": "error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            yield f"data: {json.dumps(error_update)}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )

async def register_default_agents():
    """Register default agents on startup"""
    if not agent_registry:
        return
    
    default_agents = [
        {
            "id": "langchain_qa",
            "name": "LangChain Q&A Agent",
            "description": "Question answering agent using LangChain",
            "framework": "langchain",
            "capabilities": ["question_answering", "text_generation"],
            "endpoint": "http://localhost:8001/qa",
            "status": "active"
        },
        {
            "id": "autogen_coder",
            "name": "AutoGen Coding Agent",
            "description": "Code generation agent using AutoGen",
            "framework": "autogen",
            "capabilities": ["code_generation", "code_review"],
            "endpoint": "http://localhost:8002/code",
            "status": "active"
        },
        {
            "id": "custom_analyzer",
            "name": "Custom Analysis Agent",
            "description": "Custom data analysis agent",
            "framework": "custom",
            "capabilities": ["data_analysis", "visualization"],
            "endpoint": "http://localhost:8003/analyze",
            "status": "active"
        }
    ]
    
    for agent_data in default_agents:
        try:
            agent = Agent(**agent_data)
            await agent_registry.register_agent(agent)
            logger.info(f"Registered default agent: {agent.id}")
        except Exception as e:
            logger.warning(f"Failed to register default agent {agent_data['id']}: {str(e)}")

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for debugging and monitoring"""
    start_time = datetime.utcnow()
    
    response = await call_next(request)
    
    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds()
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {duration:.3f}s"
    )
    
    return response

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 