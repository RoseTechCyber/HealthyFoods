"""
Orders API endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from typing import List, Optional
import uuid
from datetime import datetime

from app.models.schemas import Order, OrderStatus, OrderItem
from app.services.ai_agent import AIAgentOrchestrator
from app.services.azure_services import AzurePowerAutomateService, AzureServiceBusService

router = APIRouter()


@router.post("/", response_model=Order)
async def create_order(order: Order, request: Request):
    """
    Create a new food order
    AI Agent validates and processes the order
    """
    # Generate order ID
    order.id = str(uuid.uuid4())
    order.created_at = datetime.now()
    order.updated_at = datetime.now()
    
    # Get AI Agent from app state
    ai_orchestrator: AIAgentOrchestrator = request.app.state.ai_orchestrator
    
    # Validate order with AI Agent
    validation_result = await ai_orchestrator.validate_order(order)
    
    if not validation_result["is_valid"]:
        raise HTTPException(
            status_code=400,
            detail=f"Order validation failed: {', '.join(validation_result['issues'])}"
        )
    
    # Set order status
    order.status = OrderStatus.VALIDATED
    order.updated_at = datetime.now()
    
    # Trigger Azure Power Automate workflow
    power_automate = AzurePowerAutomateService()
    await power_automate.trigger_order_workflow(order.model_dump())
    
    # Send message to Azure Service Bus
    service_bus = AzureServiceBusService()
    await service_bus.send_message({
        "order_id": order.id,
        "type": "order_created",
        "timestamp": order.created_at.isoformat()
    })
    
    return order


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """
    Get order details by ID
    """
    # In production, retrieve from database
    raise HTTPException(status_code=404, detail="Order not found")


@router.get("/", response_model=List[Order])
async def list_orders(
    customer_id: Optional[str] = None,
    status: Optional[OrderStatus] = None,
    limit: int = 10
):
    """
    List orders with optional filters
    """
    # In production, retrieve from database with filters
    return []


@router.put("/{order_id}/status")
async def update_order_status(order_id: str, status: OrderStatus):
    """
    Update order status
    """
    # In production, update in database
    return {
        "order_id": order_id,
        "status": status,
        "updated_at": datetime.now().isoformat()
    }


@router.post("/{order_id}/cancel")
async def cancel_order(order_id: str):
    """
    Cancel an order
    """
    # In production, validate cancellation and update status
    return {
        "order_id": order_id,
        "status": OrderStatus.CANCELLED,
        "cancelled_at": datetime.now().isoformat()
    }


@router.get("/{order_id}/track")
async def track_order(order_id: str):
    """
    Track order status and delivery in real-time
    """
    # In production, integrate with delivery tracking service
    return {
        "order_id": order_id,
        "status": "in_transit",
        "current_location": {"lat": 40.7128, "lng": -74.0060},
        "estimated_delivery": "2026-02-19T15:30:00",
        "updates": [
            {"timestamp": "2026-02-19T14:00:00", "status": "Order received"},
            {"timestamp": "2026-02-19T14:30:00", "status": "Preparing"},
            {"timestamp": "2026-02-19T15:00:00", "status": "Out for delivery"}
        ]
    }
