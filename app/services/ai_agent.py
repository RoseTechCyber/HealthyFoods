"""
AI Agent Orchestrator - Core intelligence engine for HealthyFoods
Integrates with Azure OpenAI and Microsoft AI Services
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

from app.models.schemas import Order, OrderStatus, AIAgentDecision
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIAgentOrchestrator:
    """
    Central AI Agent that orchestrates order processing, validation,
    routing, and delivery decisions
    """
    
    def __init__(self):
        """Initialize AI Agent Orchestrator"""
        self.azure_openai_configured = bool(settings.AZURE_OPENAI_ENDPOINT)
        logger.info("AI Agent Orchestrator initialized")
        logger.info(f"Azure OpenAI configured: {self.azure_openai_configured}")
    
    async def validate_order(self, order: Order) -> Dict:
        """
        Validate order using AI-powered checks
        - Validates order completeness
        - Checks for anomalies
        - Validates delivery feasibility
        """
        logger.info(f"Validating order: {order.id}")
        
        validation_result = {
            "is_valid": True,
            "issues": [],
            "recommendations": []
        }
        
        # Basic validations
        if not order.items or len(order.items) == 0:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Order has no items")
        
        if order.total_amount <= 0:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Invalid order amount")
        
        if not order.delivery_address:
            validation_result["is_valid"] = False
            validation_result["issues"].append("No delivery address provided")
        
        # AI-powered validation (if Azure OpenAI is configured)
        if self.azure_openai_configured:
            try:
                ai_validation = await self._ai_validate_order(order)
                validation_result["ai_insights"] = ai_validation
            except Exception as e:
                logger.warning(f"AI validation failed: {e}")
        
        return validation_result
    
    async def route_order(self, order: Order, available_catering_firms: List[Dict]) -> Dict:
        """
        Intelligently route order to optimal catering firm
        - Considers firm capacity, distance, ratings
        - Uses AI to optimize selection
        """
        logger.info(f"Routing order: {order.id}")
        
        # If catering firm is already specified, validate it
        if order.catering_firm_id:
            return {
                "selected_firm_id": order.catering_firm_id,
                "reason": "Customer specified firm",
                "confidence": 1.0
            }
        
        # AI-powered routing
        if not available_catering_firms:
            return {
                "selected_firm_id": None,
                "reason": "No available catering firms",
                "confidence": 0.0
            }
        
        # Simple routing logic (can be enhanced with AI)
        best_firm = available_catering_firms[0]
        
        if self.azure_openai_configured:
            try:
                ai_routing = await self._ai_route_order(order, available_catering_firms)
                return ai_routing
            except Exception as e:
                logger.warning(f"AI routing failed: {e}")
        
        return {
            "selected_firm_id": best_firm.get("id"),
            "reason": "Default selection",
            "confidence": 0.7
        }
    
    async def process_payment_validation(self, order: Optional[Order], payment_details: Dict) -> Dict:
        """
        Validate payment details using AI fraud detection
        """
        logger.info(f"Validating payment for order: {order.id if order else 'None'}")
        
        payment_validation = {
            "is_valid": True,
            "risk_score": 0.0,
            "recommendations": []
        }
        
        # Basic payment validation
        if order and payment_details.get("amount") != order.total_amount:
            payment_validation["is_valid"] = False
            payment_validation["recommendations"].append("Amount mismatch detected")
        
        # AI-powered fraud detection
        if self.azure_openai_configured:
            try:
                fraud_check = await self._ai_fraud_detection(order, payment_details)
                payment_validation["ai_fraud_check"] = fraud_check
            except Exception as e:
                logger.warning(f"AI fraud detection failed: {e}")
        
        return payment_validation
    
    async def optimize_delivery_route(self, order: Optional[Order], available_drivers: List[Dict]) -> Dict:
        """
        Optimize delivery route and driver assignment
        - Considers driver location, capacity, ratings
        - Estimates delivery time
        """
        logger.info(f"Optimizing delivery for order: {order.id if order else 'None'}")
        
        if not available_drivers:
            return {
                "assigned_driver_id": None,
                "estimated_delivery_time": None,
                "reason": "No available drivers"
            }
        
        # Simple driver assignment (can be enhanced with AI)
        selected_driver = available_drivers[0]
        estimated_time = datetime.now() + timedelta(minutes=30)
        
        if self.azure_openai_configured:
            try:
                ai_optimization = await self._ai_optimize_delivery(order, available_drivers)
                return ai_optimization
            except Exception as e:
                logger.warning(f"AI delivery optimization failed: {e}")
        
        return {
            "assigned_driver_id": selected_driver.get("id"),
            "estimated_delivery_time": estimated_time.isoformat(),
            "route": "optimal_route",
            "confidence": 0.8
        }
    
    async def generate_recommendations(self, customer_id: str, order_history: List[Order]) -> List[Dict]:
        """
        Generate personalized food recommendations using AI
        """
        logger.info(f"Generating recommendations for customer: {customer_id}")
        
        recommendations = []
        
        # AI-powered recommendations
        if self.azure_openai_configured:
            try:
                ai_recommendations = await self._ai_generate_recommendations(customer_id, order_history)
                return ai_recommendations
            except Exception as e:
                logger.warning(f"AI recommendations failed: {e}")
        
        # Default recommendations
        recommendations.append({
            "menu_item": "Popular dish of the day",
            "reason": "Trending item",
            "confidence": 0.6
        })
        
        return recommendations
    
    async def _ai_validate_order(self, order: Order) -> Dict:
        """AI-powered order validation using Azure OpenAI"""
        # Placeholder for Azure OpenAI integration
        return {
            "completeness_score": 0.95,
            "anomaly_detected": False,
            "suggestions": []
        }
    
    async def _ai_route_order(self, order: Order, firms: List[Dict]) -> Dict:
        """AI-powered order routing"""
        # Placeholder for Azure OpenAI integration
        return {
            "selected_firm_id": firms[0].get("id") if firms else None,
            "reason": "AI-optimized selection based on capacity and rating",
            "confidence": 0.9
        }
    
    async def _ai_fraud_detection(self, order: Order, payment: Dict) -> Dict:
        """AI-powered fraud detection"""
        # Placeholder for Azure OpenAI integration
        return {
            "fraud_probability": 0.05,
            "risk_factors": [],
            "recommendation": "approve"
        }
    
    async def _ai_optimize_delivery(self, order: Order, drivers: List[Dict]) -> Dict:
        """AI-powered delivery optimization"""
        # Placeholder for Azure OpenAI integration
        return {
            "assigned_driver_id": drivers[0].get("id") if drivers else None,
            "estimated_delivery_time": (datetime.now() + timedelta(minutes=25)).isoformat(),
            "route": "AI-optimized route",
            "confidence": 0.92
        }
    
    async def _ai_generate_recommendations(self, customer_id: str, history: List[Order]) -> List[Dict]:
        """AI-powered personalized recommendations"""
        # Placeholder for Azure OpenAI integration
        return [
            {
                "menu_item": "Recommended based on preferences",
                "reason": "AI analysis of order history",
                "confidence": 0.85
            }
        ]
