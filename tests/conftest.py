"""
Test configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def sample_customer():
    """Sample customer data"""
    return {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "+1234567890",
        "address": "123 Test St, Test City, TS",
        "preferences": {
            "dietary": ["vegetarian"],
            "spice_level": "mild"
        }
    }


@pytest.fixture
def sample_order():
    """Sample order data"""
    return {
        "customer_id": "test_customer_123",
        "catering_firm_id": "test_firm_456",
        "items": [
            {
                "menu_item_id": "item_789",
                "menu_item_name": "Test Salad",
                "quantity": 2,
                "unit_price": 12.99
            }
        ],
        "total_amount": 25.98,
        "delivery_address": "123 Test St, Test City, TS"
    }


@pytest.fixture
def sample_payment():
    """Sample payment data"""
    return {
        "order_id": "test_order_123",
        "amount": 25.98,
        "payment_method": "credit_card"
    }
