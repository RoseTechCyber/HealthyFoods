"""
Main application entry point for HealthyFoods AI Agentic Web Application
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import orders, customers, catering_firms, payments, delivery
from app.core.config import settings
from app.core.security import setup_security
from app.services.ai_agent import AIAgentOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting HealthyFoods AI Agentic Web Application")
    
    # Initialize AI Agent Orchestrator
    ai_orchestrator = AIAgentOrchestrator()
    app.state.ai_orchestrator = ai_orchestrator
    
    logger.info("AI Agent Orchestrator initialized")
    
    yield
    
    logger.info("Shutting down HealthyFoods Application")


# Create FastAPI application
app = FastAPI(
    title="HealthyFoods AI Agentic Platform",
    description="Real-time, 24/7 intelligent food ordering and delivery system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup security middleware
setup_security(app)

# Include routers
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(catering_firms.router, prefix="/api/v1/catering-firms", tags=["Catering Firms"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(delivery.router, prefix="/api/v1/delivery", tags=["Delivery"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to HealthyFoods AI Agentic Platform",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "HealthyFoods",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
