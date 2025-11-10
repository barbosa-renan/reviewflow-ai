"""
Configurações para o sistema ReviewFlow AI.
"""

import os
from typing import Optional


class Settings:
    """Configurações da aplicação."""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_RELOAD: bool = os.getenv("API_RELOAD", "true").lower() == "true"
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Application Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_BATCH_SIZE: int = int(os.getenv("MAX_BATCH_SIZE", "100"))
    
    # Database Configuration (para futuro uso)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Cache Configuration (para futuro uso)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    
    def __init__(self):
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")


# Instância global das configurações
settings = Settings()