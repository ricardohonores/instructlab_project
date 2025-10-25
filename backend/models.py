"""
Modelos Pydantic para validación de datos
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class ChatMessage(BaseModel):
    """Mensaje individual en una conversación"""
    role: str = Field(..., description="Rol del mensaje: 'user' o 'assistant'")
    content: str = Field(..., description="Contenido del mensaje")
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in ['user', 'assistant', 'system']:
            raise ValueError('El rol debe ser user, assistant o system')
        return v

class ChatRequest(BaseModel):
    """Request para el endpoint de chat"""
    message: str = Field(..., min_length=1, max_length=2000, description="Mensaje del usuario")
    conversation_history: Optional[List[ChatMessage]] = Field(default=None, description="Historial de conversación")
    max_tokens: Optional[int] = Field(default=500, ge=1, le=2000, description="Máximo de tokens a generar")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Temperatura para generación")
    stream: Optional[bool] = Field(default=False, description="Streaming de respuesta")
    
    model_config = {  # ✅ Actualizado
        "json_schema_extra": {
            "example": {
                "message": "¿Qué es la personalización del aprendizaje con IA?",
                "max_tokens": 500,
                "temperature": 0.7
            }
        }
    }

class ChatResponse(BaseModel):
    """Response del endpoint de chat"""
    response: str = Field(..., description="Respuesta del modelo")
    model: str = Field(..., description="Nombre del modelo usado")
    tokens_used: int = Field(..., description="Total de tokens usados")
    prompt_tokens: int = Field(..., description="Tokens del prompt")
    completion_tokens: int = Field(..., description="Tokens de la respuesta")
    latency_seconds: float = Field(..., description="Tiempo de respuesta en segundos")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de la respuesta")
    
    model_config = {  # ✅ Actualizado
        "json_schema_extra": {
            "example": {
                "response": "La personalización del aprendizaje con IA...",
                "model": "granite-7b-lab",
                "tokens_used": 195,
                "prompt_tokens": 45,
                "completion_tokens": 150,
                "latency_seconds": 1.23,
                "timestamp": "2024-10-23T10:30:00"
            }
        }
    }

class HealthResponse(BaseModel):
    """Response del health check"""
    status: str
    vllm_status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str

class ErrorResponse(BaseModel):
    """Response de error estandarizada"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
