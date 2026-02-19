"""
Tests for orders API
"""

import pytest


def test_create_order(client, sample_order):
    """Test creating a new order"""
    response = client.post("/api/v1/orders", json=sample_order)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "validated"


def test_create_order_validation_fails_empty_items(client, sample_order):
    """Test order validation fails with empty items"""
    sample_order["items"] = []
    response = client.post("/api/v1/orders", json=sample_order)
    assert response.status_code == 400


def test_create_order_validation_fails_invalid_amount(client, sample_order):
    """Test order validation fails with invalid amount"""
    sample_order["total_amount"] = 0
    response = client.post("/api/v1/orders", json=sample_order)
    assert response.status_code == 400
