"""
Configuración del backend
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings  # ✅ Correcto para pydantic v2.11+

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API Settings
    APP_NAME: str = "Chatbot Educativo API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # vLLM Settings
    VLLM_API_URL: str = "http://localhost:8080"
    VLLM_MODEL_NAME: str = "/home/honores/.local/share/instructlab/checkpoints/hf_format/samples_0"
    VLLM_TIMEOUT: int = 120
    
    # Generation Settings
    DEFAULT_MAX_TOKENS: int = 500
    DEFAULT_TEMPERATURE: float = 0.7
    MAX_TOKENS_LIMIT: int = 2000
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_PERIOD: int = 60
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    
    # System Prompt
    SYSTEM_PROMPT: str = "Eres un asistente experto en Inteligencia Artificial aplicada a la educación. Respondes de manera clara, precisa y pedagógica."
    
    model_config = {  # ✅ Cambiado de 'class Config' a 'model_config'
        "env_file": ".env",
        "case_sensitive": True
    }

# Instancia global de configuración
settings = Settings()
