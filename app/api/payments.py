"""
Payments API endpoints
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import APIRouter, HTTPException, Request
from typing import List, Optional
import uuid
from datetime import datetime

from app.models.schemas import Payment, PaymentStatus
from app.services.ai_agent import AIAgentOrchestrator
from app.services.azure_services import AzurePowerAutomateService

router = APIRouter()


@router.post("/", response_model=Payment)
async def process_payment(payment: Payment, request: Request):
    """
    Process payment for an order
    Uses AI Agent for fraud detection
    """
    payment.id = str(uuid.uuid4())
    payment.created_at = datetime.now()
    payment.status = PaymentStatus.PROCESSING
    
    # Get AI Agent from app state
    ai_orchestrator: AIAgentOrchestrator = request.app.state.ai_orchestrator
    
    # Validate payment with AI-powered fraud detection
    validation_result = await ai_orchestrator.process_payment_validation(
        order=None,  # In production, retrieve order from database
        payment_details=payment.model_dump()
    )
    
    if not validation_result["is_valid"]:
        payment.status = PaymentStatus.FAILED
        raise HTTPException(
            status_code=400,
            detail="Payment validation failed"
        )
    
    # Process payment with payment gateway
    # In production, integrate with actual payment gateway (Stripe, PayPal, etc.)
    
    payment.status = PaymentStatus.COMPLETED
    payment.completed_at = datetime.now()
    payment.transaction_id = f"txn_{uuid.uuid4()}"
    
    # Trigger Azure Power Automate workflow
    power_automate = AzurePowerAutomateService()
    await power_automate.trigger_payment_workflow(payment.model_dump())
    
    return payment


@router.get("/{payment_id}", response_model=Payment)
async def get_payment(payment_id: str):
    """
    Get payment details by ID
    """
    # In production, retrieve from database
    raise HTTPException(status_code=404, detail="Payment not found")


@router.get("/order/{order_id}", response_model=List[Payment])
async def get_order_payments(order_id: str):
    """
    Get all payments for an order
    """
    # In production, retrieve from database
    return []


@router.post("/{payment_id}/refund")
async def refund_payment(payment_id: str, amount: Optional[float] = None):
    """
    Refund a payment (full or partial)
    """
    # In production, process refund with payment gateway
    return {
        "payment_id": payment_id,
        "status": PaymentStatus.REFUNDED,
        "refund_amount": amount,
        "refunded_at": datetime.now().isoformat()
    }


@router.get("/{payment_id}/receipt")
async def get_payment_receipt(payment_id: str):
    """
    Get payment receipt
    """
    # In production, generate and return receipt
    return {
        "payment_id": payment_id,
        "receipt_url": f"https://receipts.healthyfoods.com/{payment_id}",
        "generated_at": datetime.now().isoformat()
    }
