"""
Configuration settings for HealthyFoods2 application
Integrates with Azure services and Microsoft Foundry
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application settings
    APP_NAME: str = "HealthyFoods2"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Azure OpenAI / AI Services
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    
    # Azure Content Safety
    AZURE_CONTENT_SAFETY_ENDPOINT: str = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    AZURE_CONTENT_SAFETY_KEY: str = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    
    # Azure Application Insights (Monitoring)
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "")
    
    # Azure Key Vault (Secrets Management)
    AZURE_KEY_VAULT_URL: str = os.getenv("AZURE_KEY_VAULT_URL", "")
    
    # Azure Storage (for data persistence)
    AZURE_STORAGE_CONNECTION_STRING: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    AZURE_STORAGE_CONTAINER: str = "healthyfoods-data"
    
    # Azure Service Bus (for message queuing)
    AZURE_SERVICE_BUS_CONNECTION_STRING: str = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING", "")
    AZURE_SERVICE_BUS_QUEUE_NAME: str = "orders-queue"
    
    # Azure MCP (Model Context Protocol)
    AZURE_MCP_ENDPOINT: str = os.getenv("AZURE_MCP_ENDPOINT", "")
    
    # Payment processing
    PAYMENT_GATEWAY_API_KEY: str = os.getenv("PAYMENT_GATEWAY_API_KEY", "")
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./healthyfoods.db")
    
    # Redis cache
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
