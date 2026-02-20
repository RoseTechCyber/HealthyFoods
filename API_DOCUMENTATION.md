# API Documentation - HealthyFoods

## Base URL

```
Production: https://healthyfoods.azurewebsites.net
Development: http://localhost:8000
```

## Authentication

Most endpoints require authentication using Bearer token:

```
Authorization: Bearer {your-token}
```

## Endpoints

### Health & Status

#### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "HealthyFoods",
  "version": "1.0.0"
}
```

---

## Orders

### POST /api/v1/orders
Create a new food order

**Request Body:**
```json
{
  "customer_id": "cust123",
  "catering_firm_id": "firm456",
  "items": [
    {
      "menu_item_id": "item789",
      "menu_item_name": "Grilled Chicken Salad",
      "quantity": 2,
      "unit_price": 12.99,
      "special_instructions": "No onions"
    }
  ],
  "total_amount": 25.98,
  "delivery_address": "123 Main St, City, State"
}
```

**Response:**
```json
{
  "id": "order_abc123",
  "customer_id": "cust123",
  "status": "validated",
  "created_at": "2026-02-19T00:00:00Z",
  "estimated_delivery_time": "2026-02-19T01:30:00Z"
}
```

### GET /api/v1/orders/{order_id}
Get order details

**Response:**
```json
{
  "id": "order_abc123",
  "customer_id": "cust123",
  "catering_firm_id": "firm456",
  "status": "preparing",
  "items": [...],
  "total_amount": 25.98
}
```

### GET /api/v1/orders/{order_id}/track
Track order in real-time

**Response:**
```json
{
  "order_id": "order_abc123",
  "status": "in_transit",
  "current_location": {
    "lat": 40.7128,
    "lng": -74.0060
  },
  "estimated_delivery": "2026-02-19T15:30:00",
  "updates": [
    {
      "timestamp": "2026-02-19T14:00:00",
      "status": "Order received"
    }
  ]
}
```

---

## Customers

### POST /api/v1/customers
Register a new customer

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Main St, City, State",
  "preferences": {
    "dietary": ["vegetarian"],
    "spice_level": "mild"
  }
}
```

**Response:**
```json
{
  "id": "cust_xyz789",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2026-02-19T00:00:00Z"
}
```

### GET /api/v1/customers/{customer_id}/recommendations
Get AI-powered food recommendations

**Response:**
```json
{
  "customer_id": "cust123",
  "recommendations": [
    {
      "menu_item": "Grilled Chicken Salad",
      "catering_firm": "Healthy Bites",
      "reason": "Based on your previous orders",
      "confidence": 0.85
    }
  ]
}
```

---

## Catering Firms

### POST /api/v1/catering-firms
Register a new catering firm

**Request Body:**
```json
{
  "name": "Healthy Bites",
  "email": "contact@healthybites.com",
  "phone": "+1234567890",
  "address": "456 Food St, City, State",
  "cuisine_types": ["Italian", "Mediterranean"],
  "operating_hours": {
    "monday": "9:00-21:00",
    "tuesday": "9:00-21:00"
  }
}
```

### GET /api/v1/catering-firms/{firm_id}/menu
Get menu items for a catering firm

**Response:**
```json
[
  {
    "id": "item123",
    "name": "Grilled Chicken Salad",
    "description": "Fresh salad with grilled chicken",
    "price": 12.99,
    "category": "Main Course",
    "dietary_info": ["gluten-free", "high-protein"],
    "is_available": true
  }
]
```

---

## Payments

### POST /api/v1/payments
Process payment for an order

**Request Body:**
```json
{
  "order_id": "order123",
  "amount": 25.98,
  "payment_method": "credit_card"
}
```

**Response:**
```json
{
  "id": "payment_xyz",
  "order_id": "order123",
  "amount": 25.98,
  "status": "completed",
  "transaction_id": "txn_abc123",
  "completed_at": "2026-02-19T00:00:00Z"
}
```

### POST /api/v1/payments/{payment_id}/refund
Refund a payment

**Request Body:**
```json
{
  "amount": 25.98
}
```

---

## Delivery

### POST /api/v1/delivery
Assign delivery for an order

**Request Body:**
```json
{
  "order_id": "order123"
}
```

**Response:**
```json
{
  "id": "delivery_xyz",
  "order_id": "order123",
  "driver_id": "driver456",
  "status": "assigned",
  "estimated_arrival": "2026-02-19T15:30:00Z"
}
```

### GET /api/v1/delivery/{delivery_id}/track
Track delivery in real-time

**Response:**
```json
{
  "delivery_id": "delivery_xyz",
  "status": "in_transit",
  "current_location": {
    "lat": 40.7128,
    "lng": -74.0060
  },
  "estimated_arrival": "2026-02-19T15:30:00",
  "driver": {
    "id": "driver456",
    "name": "John Driver",
    "phone": "+1234567890"
  }
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Rate Limiting

API requests are limited to 60 requests per minute per IP address.

**Rate Limit Headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1676851200
```

---

## Webhooks

Configure webhooks to receive real-time updates about orders, payments, and deliveries.

### Webhook Events

- `order.created`
- `order.validated`
- `order.payment_confirmed`
- `order.preparing`
- `order.out_for_delivery`
- `order.delivered`
- `payment.completed`
- `payment.failed`
- `delivery.assigned`
- `delivery.picked_up`
- `delivery.delivered`

### Webhook Payload Example

```json
{
  "event": "order.created",
  "timestamp": "2026-02-19T00:00:00Z",
  "data": {
    "order_id": "order123",
    "customer_id": "cust456",
    "status": "validated"
  }
}
```

---

## SDK Examples

### Python

```python
import requests

# Create order
response = requests.post(
    "https://healthyfoods.azurewebsites.net/api/v1/orders",
    json={
        "customer_id": "cust123",
        "catering_firm_id": "firm456",
        "items": [...],
        "total_amount": 25.98,
        "delivery_address": "123 Main St"
    },
    headers={"Authorization": "Bearer {token}"}
)

order = response.json()
print(f"Order created: {order['id']}")
```

### JavaScript

```javascript
// Create order
const response = await fetch('https://healthyfoods.azurewebsites.net/api/v1/orders', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {token}'
  },
  body: JSON.stringify({
    customer_id: 'cust123',
    catering_firm_id: 'firm456',
    items: [...],
    total_amount: 25.98,
    delivery_address: '123 Main St'
  })
});

const order = await response.json();
console.log(`Order created: ${order.id}`);
```

---

For more information, visit the interactive API documentation at `/docs` endpoint.
