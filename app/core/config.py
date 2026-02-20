"""
Configuration settings for HealthyFoods application
Integrates with Azure services and Microsoft Foundry
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pydantic import Field
import sys


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    # Application settings
    APP_NAME: str = "HealthyFoods"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Security settings - SECRET_KEY must be provided via environment variable
    SECRET_KEY: str = Field(..., description="Secret key for encryption and signing. Must be set in environment.")
    API_KEYS: Optional[List[str]] = Field(default=None, description="List of valid API keys for authentication")
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Azure OpenAI / AI Services
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    
    # Azure Content Safety
    AZURE_CONTENT_SAFETY_ENDPOINT: str = ""
    AZURE_CONTENT_SAFETY_KEY: str = ""
    
    # Azure Application Insights (Monitoring)
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = ""
    
    # Azure Key Vault (Secrets Management)
    AZURE_KEY_VAULT_URL: str = ""
    
    # Azure Storage (for data persistence)
    AZURE_STORAGE_CONNECTION_STRING: str = ""
    AZURE_STORAGE_CONTAINER: str = "healthyfoods-data"
    
    # Azure Service Bus (for message queuing)
    AZURE_SERVICE_BUS_CONNECTION_STRING: str = ""
    AZURE_SERVICE_BUS_QUEUE_NAME: str = "orders-queue"
    
    # Azure MCP (Model Context Protocol)
    AZURE_MCP_ENDPOINT: str = ""
    
    # Payment processing
    PAYMENT_GATEWAY_API_KEY: str = ""
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./healthyfoods.db"
    
    # Redis cache
    REDIS_URL: str = "redis://localhost:6379"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
try:
    settings = Settings()
except Exception as e:
    print(f"Error: Failed to load settings. SECRET_KEY environment variable is required.", file=sys.stderr)
    print(f"Details: {e}", file=sys.stderr)
    sys.exit(1)
