"""
Delivery API endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from typing import List, Optional
import uuid
from datetime import datetime

from app.models.schemas import Delivery, DeliveryStatus
from app.services.ai_agent import AIAgentOrchestrator
from app.services.azure_services import AzurePowerAutomateService

router = APIRouter()


@router.post("/", response_model=Delivery)
async def assign_delivery(delivery: Delivery, request: Request):
    """
    Assign delivery for an order
    Uses AI Agent for optimal driver selection and route optimization
    """
    delivery.id = str(uuid.uuid4())
    delivery.status = DeliveryStatus.PENDING
    
    # Get AI Agent from app state
    ai_orchestrator: AIAgentOrchestrator = request.app.state.ai_orchestrator
    
    # Get available drivers (in production, from database)
    available_drivers = [
        {"id": "driver1", "name": "Driver 1", "location": {"lat": 40.7128, "lng": -74.0060}},
        {"id": "driver2", "name": "Driver 2", "location": {"lat": 40.7589, "lng": -73.9851}}
    ]
    
    # Optimize delivery with AI Agent
    optimization_result = await ai_orchestrator.optimize_delivery_route(
        order=None,  # In production, retrieve order from database
        available_drivers=available_drivers
    )
    
    delivery.driver_id = optimization_result["assigned_driver_id"]
    delivery.estimated_arrival = datetime.fromisoformat(optimization_result["estimated_delivery_time"]) if optimization_result.get("estimated_delivery_time") else None
    delivery.status = DeliveryStatus.ASSIGNED
    
    # Trigger Azure Power Automate workflow
    power_automate = AzurePowerAutomateService()
    await power_automate.trigger_delivery_workflow(delivery.dict())
    
    return delivery


@router.get("/{delivery_id}", response_model=Delivery)
async def get_delivery(delivery_id: str):
    """
    Get delivery details by ID
    """
    # In production, retrieve from database
    raise HTTPException(status_code=404, detail="Delivery not found")


@router.get("/order/{order_id}", response_model=Delivery)
async def get_order_delivery(order_id: str):
    """
    Get delivery for an order
    """
    # In production, retrieve from database
    raise HTTPException(status_code=404, detail="Delivery not found")


@router.put("/{delivery_id}/status")
async def update_delivery_status(delivery_id: str, status: DeliveryStatus):
    """
    Update delivery status
    """
    # In production, update in database
    return {
        "delivery_id": delivery_id,
        "status": status,
        "updated_at": datetime.now().isoformat()
    }


@router.post("/{delivery_id}/location")
async def update_delivery_location(delivery_id: str, latitude: float, longitude: float):
    """
    Update delivery real-time location
    """
    # In production, update location in database and broadcast to customer
    return {
        "delivery_id": delivery_id,
        "current_location": {"lat": latitude, "lng": longitude},
        "updated_at": datetime.now().isoformat()
    }


@router.get("/{delivery_id}/track")
async def track_delivery_realtime(delivery_id: str):
    """
    Track delivery in real-time
    """
    # In production, return real-time tracking data
    return {
        "delivery_id": delivery_id,
        "status": DeliveryStatus.IN_TRANSIT,
        "current_location": {"lat": 40.7128, "lng": -74.0060},
        "estimated_arrival": "2026-02-19T15:30:00",
        "driver": {
            "id": "driver1",
            "name": "John Driver",
            "phone": "+1234567890"
        },
        "route": []
    }


@router.post("/{delivery_id}/complete")
async def complete_delivery(delivery_id: str, signature: Optional[str] = None):
    """
    Mark delivery as completed
    """
    # In production, update status and save signature
    return {
        "delivery_id": delivery_id,
        "status": DeliveryStatus.DELIVERED,
        "delivered_at": datetime.now().isoformat(),
        "signature_captured": bool(signature)
    }
