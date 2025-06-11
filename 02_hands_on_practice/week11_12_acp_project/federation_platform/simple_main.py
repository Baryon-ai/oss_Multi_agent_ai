"""
Simple ACP Federation Platform - Standalone FastAPI Server
Agent Communication Protocol implementation (simplified version)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from typing import List, Dict, Any
from datetime import datetime
import uuid

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple in-memory storage
agents_db = {}
runs_db = {}

# Create FastAPI app
app = FastAPI(
    title="ACP Federation Platform",
    description="Agent Communication Protocol implementation (Simplified)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize default agents on startup"""
    logger.info("Starting ACP Federation Platform...")
    
    # Register default agents
    default_agents = [
        {
            "id": "analytics-agent",
            "name": "Analytics Agent",
            "description": "Data analysis and visualization agent",
            "framework": "custom",
            "capabilities": ["data_analysis", "visualization"],
            "status": "active",
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "id": "langchain-qa",
            "name": "LangChain Q&A Agent",
            "description": "Question answering using LangChain",
            "framework": "langchain",
            "capabilities": ["question_answering", "text_generation"],
            "status": "active",
            "created_at": datetime.utcnow().isoformat()
        }
    ]
    
    for agent in default_agents:
        agents_db[agent["id"]] = agent
        logger.info(f"Registered agent: {agent['id']}")
    
    logger.info("ACP Federation Platform started successfully")

@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "name": "ACP Federation Platform",
        "version": "1.0.0",
        "description": "Agent Communication Protocol implementation",
        "endpoints": {
            "agents": "/agents",
            "health": "/health"
        },
        "timestamp": datetime.utcnow().isoformat(),
        "active_agents": len(agents_db)
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents_count": len(agents_db),
        "runs_count": len(runs_db)
    }

@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": list(agents_db.values()),
        "count": len(agents_db)
    }

@app.get("/agents/{agent_id}")
async def get_agent_detail(agent_id: str):
    """Get agent details (ACP standard endpoint)"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    return agents_db[agent_id]

@app.post("/agents/{agent_id}/runs")
async def create_agent_run(agent_id: str, request_data: Dict[str, Any]):
    """Create and execute agent run (ACP standard endpoint)"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    # Create run
    run_id = str(uuid.uuid4())
    
    # Simulate processing
    run_data = {
        "id": run_id,
        "agent_id": agent_id,
        "status": "completed",
        "input": request_data.get("input", []),
        "output": [
            {
                "parts": [
                    {
                        "content": f"Processed by {agent_id}: {request_data.get('input', 'No input')}",
                        "content_type": "text/plain"
                    }
                ]
            }
        ],
        "created_at": datetime.utcnow().isoformat(),
        "completed_at": datetime.utcnow().isoformat()
    }
    
    runs_db[run_id] = run_data
    
    return {
        "run_id": run_id,
        "status": "completed",
        "agent_id": agent_id,
        "created_at": run_data["created_at"]
    }

@app.get("/agents/{agent_id}/runs/{run_id}")
async def get_run_status(agent_id: str, run_id: str):
    """Get run status and results (ACP standard endpoint)"""
    if run_id not in runs_db:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    
    run = runs_db[run_id]
    if run["agent_id"] != agent_id:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found for agent {agent_id}")
    
    return run

@app.get("/metrics")
async def metrics():
    """Platform metrics endpoint"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "agents": {
            "total": len(agents_db),
            "active": len([a for a in agents_db.values() if a["status"] == "active"])
        },
        "runs": {
            "total": len(runs_db),
            "completed": len([r for r in runs_db.values() if r["status"] == "completed"])
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 