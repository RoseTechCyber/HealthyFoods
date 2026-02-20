"""
Data models for HealthyFoods application
"""

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "pending"
    VALIDATED = "validated"
    PAYMENT_PROCESSING = "payment_processing"
    PAYMENT_CONFIRMED = "payment_confirmed"
    ASSIGNED = "assigned"
    PREPARING = "preparing"
    READY_FOR_DELIVERY = "ready_for_delivery"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class DeliveryStatus(str, Enum):
    """Delivery status enumeration"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"


class Customer(BaseModel):
    """Customer model"""
    id: Optional[str] = None
    name: str
    email: EmailStr
    phone: str
    address: str
    preferences: Optional[dict] = None
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "address": "123 Main St, City, State",
                "preferences": {"dietary": ["vegetarian"], "spice_level": "mild"}
            }
        }
    )


class CateringFirm(BaseModel):
    """Catering Firm model"""
    id: Optional[str] = None
    name: str
    email: EmailStr
    phone: str
    address: str
    cuisine_types: List[str]
    rating: Optional[float] = 0.0
    is_active: bool = True
    operating_hours: Optional[dict] = None
    menu_items: Optional[List[dict]] = None
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Healthy Bites",
                "email": "contact@healthybites.com",
                "phone": "+1234567890",
                "address": "456 Food St, City, State",
                "cuisine_types": ["Italian", "Mediterranean"],
                "operating_hours": {"monday": "9:00-21:00", "tuesday": "9:00-21:00"}
            }
        }
    )


class MenuItem(BaseModel):
    """Menu item model"""
    id: Optional[str] = None
    catering_firm_id: str
    name: str
    description: str
    price: float
    category: str
    dietary_info: Optional[List[str]] = None
    ingredients: Optional[List[str]] = None
    is_available: bool = True
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "catering_firm_id": "firm123",
                "name": "Grilled Chicken Salad",
                "description": "Fresh salad with grilled chicken",
                "price": 12.99,
                "category": "Main Course",
                "dietary_info": ["gluten-free", "high-protein"]
            }
        }
    )


class OrderItem(BaseModel):
    """Order item model"""
    menu_item_id: str
    menu_item_name: str
    quantity: int
    unit_price: float
    special_instructions: Optional[str] = None


class Order(BaseModel):
    """Order model"""
    id: Optional[str] = None
    customer_id: str
    catering_firm_id: str
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    delivery_address: str
    delivery_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    estimated_delivery_time: Optional[datetime] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_id": "cust123",
                "catering_firm_id": "firm123",
                "items": [
                    {
                        "menu_item_id": "item123",
                        "menu_item_name": "Grilled Chicken Salad",
                        "quantity": 2,
                        "unit_price": 12.99
                    }
                ],
                "total_amount": 25.98,
                "delivery_address": "123 Main St, City, State"
            }
        }
    )


class Payment(BaseModel):
    """Payment model"""
    id: Optional[str] = None
    order_id: str
    amount: float
    payment_method: str
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "order_id": "order123",
                "amount": 25.98,
                "payment_method": "credit_card",
                "status": "completed"
            }
        }
    )


class Delivery(BaseModel):
    """Delivery model"""
    id: Optional[str] = None
    order_id: str
    driver_id: Optional[str] = None
    status: DeliveryStatus = DeliveryStatus.PENDING
    pickup_time: Optional[datetime] = None
    delivery_time: Optional[datetime] = None
    current_location: Optional[dict] = None
    estimated_arrival: Optional[datetime] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "order_id": "order123",
                "driver_id": "driver456",
                "status": "in_transit",
                "estimated_arrival": "2026-02-19T15:30:00"
            }
        }
    )


class AIAgentDecision(BaseModel):
    """AI Agent decision model"""
    order_id: str
    decision_type: str
    recommendation: str
    confidence_score: float
    reasoning: str
    alternative_options: Optional[List[dict]] = None
    created_at: Optional[datetime] = None
