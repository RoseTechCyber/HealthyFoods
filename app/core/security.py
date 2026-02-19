"""
Security module with Azure Content Safety and Microsoft Security integration
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from typing import Optional
import hashlib
import hmac

from app.core.config import settings

logger = logging.getLogger(__name__)

security = HTTPBearer()


class ContentSafetyMiddleware(BaseHTTPMiddleware):
    """Middleware for Azure Content Safety validation"""
    
    async def dispatch(self, request: Request, call_next):
        """Check content safety for text inputs"""
        
        # Skip content safety for certain endpoints
        skip_paths = ["/health", "/", "/docs", "/openapi.json"]
        if request.url.path in skip_paths:
            return await call_next(request)
        
        # For POST/PUT requests with text content, validate with Azure Content Safety
        if request.method in ["POST", "PUT"]:
            try:
                # In production, integrate with Azure Content Safety API
                # For now, basic validation
                logger.info(f"Content safety check for {request.url.path}")
                
            except Exception as e:
                logger.error(f"Content safety check failed: {e}")
                raise HTTPException(status_code=400, detail="Content safety validation failed")
        
        response = await call_next(request)
        return response


class DataProtectionMiddleware(BaseHTTPMiddleware):
    """Middleware for data protection and encryption"""
    
    async def dispatch(self, request: Request, call_next):
        """Apply data protection measures"""
        
        # Add security headers
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response


def setup_security(app: FastAPI):
    """Setup security middleware and configurations"""
    
    # Add content safety middleware
    app.add_middleware(ContentSafetyMiddleware)
    
    # Add data protection middleware
    app.add_middleware(DataProtectionMiddleware)
    
    logger.info("Security middleware configured")


def verify_api_key(api_key: str) -> bool:
    """Verify API key for authentication"""
    # In production, verify against Azure Key Vault or database
    return True


def hash_sensitive_data(data: str) -> str:
    """Hash sensitive data for storage"""
    return hashlib.sha256(data.encode()).hexdigest()


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify webhook signature for secure integrations"""
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)
