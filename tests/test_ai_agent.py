"""
Tests for AI Agent Orchestrator
"""

import pytest
from app.services.ai_agent import AIAgentOrchestrator
from app.models.schemas import Order, OrderItem


@pytest.mark.asyncio
async def test_ai_agent_initialization():
    """Test AI Agent Orchestrator initialization"""
    orchestrator = AIAgentOrchestrator()
    assert orchestrator is not None


@pytest.mark.asyncio
async def test_validate_order_success():
    """Test successful order validation"""
    orchestrator = AIAgentOrchestrator()
    
    order = Order(
        customer_id="test_customer",
        catering_firm_id="test_firm",
        items=[
            OrderItem(
                menu_item_id="item1",
                menu_item_name="Test Item",
                quantity=1,
                unit_price=10.0
            )
        ],
        total_amount=10.0,
        delivery_address="123 Test St"
    )
    
    result = await orchestrator.validate_order(order)
    assert result["is_valid"] == True
    assert len(result["issues"]) == 0


@pytest.mark.asyncio
async def test_validate_order_fails_no_items():
    """Test order validation fails with no items"""
    orchestrator = AIAgentOrchestrator()
    
    order = Order(
        customer_id="test_customer",
        catering_firm_id="test_firm",
        items=[],
        total_amount=10.0,
        delivery_address="123 Test St"
    )
    
    result = await orchestrator.validate_order(order)
    assert result["is_valid"] == False
    assert "no items" in result["issues"][0].lower()


@pytest.mark.asyncio
async def test_route_order():
    """Test order routing"""
    orchestrator = AIAgentOrchestrator()
    
    order = Order(
        customer_id="test_customer",
        catering_firm_id="test_firm",
        items=[
            OrderItem(
                menu_item_id="item1",
                menu_item_name="Test Item",
                quantity=1,
                unit_price=10.0
            )
        ],
        total_amount=10.0,
        delivery_address="123 Test St"
    )
    
    available_firms = [
        {"id": "firm1", "name": "Firm 1"},
        {"id": "firm2", "name": "Firm 2"}
    ]
    
    result = await orchestrator.route_order(order, available_firms)
    assert "selected_firm_id" in result
    assert result["confidence"] >= 0


@pytest.mark.asyncio
async def test_generate_recommendations():
    """Test AI-powered recommendations"""
    orchestrator = AIAgentOrchestrator()
    
    recommendations = await orchestrator.generate_recommendations("customer123", [])
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
