"""
Customers API endpoints
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import APIRouter, HTTPException
from typing import List, Optional
import uuid
from datetime import datetime

from app.models.schemas import Customer

router = APIRouter()


@router.post("/", response_model=Customer)
async def create_customer(customer: Customer):
    """
    Register a new customer
    """
    customer.id = str(uuid.uuid4())
    customer.created_at = datetime.now()
    
    # In production, save to database
    return customer


@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    """
    Get customer details by ID
    """
    # In production, retrieve from database
    raise HTTPException(status_code=404, detail="Customer not found")


@router.get("/", response_model=List[Customer])
async def list_customers(limit: int = 10):
    """
    List customers
    """
    # In production, retrieve from database
    return []


@router.put("/{customer_id}", response_model=Customer)
async def update_customer(customer_id: str, customer: Customer):
    """
    Update customer information
    """
    customer.id = customer_id
    
    # In production, update in database
    return customer


@router.delete("/{customer_id}")
async def delete_customer(customer_id: str):
    """
    Delete a customer
    """
    # In production, soft delete in database
    return {"message": "Customer deleted", "customer_id": customer_id}


@router.get("/{customer_id}/orders")
async def get_customer_orders(customer_id: str):
    """
    Get all orders for a customer
    """
    # In production, retrieve from database
    return []


@router.get("/{customer_id}/recommendations")
async def get_customer_recommendations(customer_id: str):
    """
    Get AI-powered food recommendations for customer
    """
    # In production, use AI Agent to generate recommendations
    return {
        "customer_id": customer_id,
        "recommendations": [
            {
                "menu_item": "Grilled Chicken Salad",
                "catering_firm": "Healthy Bites",
                "reason": "Based on your previous orders",
                "confidence": 0.85
            }
        ]
    }
