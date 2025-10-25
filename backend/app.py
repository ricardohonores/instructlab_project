
"""
API Backend con FastAPI para el Chatbot Educativo
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from config import settings
from models import (
    ChatRequest, 
    ChatResponse, 
    HealthResponse, 
    ErrorResponse
)
from services.vllm_service import vllm_service

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ejecutar código al inicio y fin de la aplicación"""
    # Startup
    logger.info("🚀 Iniciando API Backend...")
    logger.info(f"📦 Conectando a vLLM en {settings.VLLM_API_URL}")
    
    # Verificar conexión con vLLM
    is_healthy = await vllm_service.check_health()
    if is_healthy:
        logger.info("✅ Conexión con vLLM exitosa")
    else:
        logger.warning("⚠️  No se pudo conectar con vLLM al iniciar")
    
    yield
    
    # Shutdown
    logger.info("👋 Apagando API Backend...")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API REST para chatbot educativo con IA",
    lifespan=lifespan
)

# ==================== CORS ====================

# Configuración CORS más permisiva para demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Explícitamente incluir OPTIONS
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache de preflight por 1 hora
)
# Exception handler global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejar excepciones no capturadas"""
    logger.error(f"Error no manejado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Error interno del servidor",
            detail=str(exc) if settings.DEBUG else None
        ).model_dump()
    )

# ==================== ENDPOINTS ====================

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "API del Chatbot Educativo",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Verificar el estado de la API y sus dependencias
    """
    vllm_healthy = await vllm_service.check_health()
    
    return HealthResponse(
        status="ok" if vllm_healthy else "degraded",
        vllm_status="connected" if vllm_healthy else "disconnected",
        version=settings.APP_VERSION
    )

@app.get("/models", tags=["Models"])
async def list_models():
    """
    Listar modelos disponibles en vLLM
    """
    try:
        models = await vllm_service.get_models()
        return models
    except Exception as e:
        logger.error(f"Error obteniendo modelos: {e}")
        raise HTTPException(
            status_code=503,
            detail="No se pudo obtener la lista de modelos"
        )

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Endpoint principal para chatear con el modelo
    
    - **message**: Mensaje del usuario (requerido)
    - **conversation_history**: Historial de mensajes previos (opcional)
    - **max_tokens**: Máximo de tokens a generar (default: 500)
    - **temperature**: Temperatura de generación (default: 0.7)
    """
    try:
        logger.info(f"📨 Nueva pregunta: {request.message[:50]}...")
        
        # Llamar al servicio vLLM
        result = await vllm_service.chat_completion(
            message=request.message,
            conversation_history=request.conversation_history,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=request.stream
        )
        
        # Construir respuesta
        usage = result.get("usage", {})
        
        response = ChatResponse(
            response=result["response"],
            model=result["model"],
            tokens_used=usage.get("total_tokens", 0),
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            latency_seconds=result["latency_seconds"]
        )
        
        logger.info(f"✅ Respuesta generada en {result['latency_seconds']}s")
        return response
        
    except httpx.TimeoutException:
        logger.error("⏱️  Timeout esperando respuesta de vLLM")
        raise HTTPException(
            status_code=504,
            detail="El modelo tardó demasiado en responder"
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"❌ Error HTTP de vLLM: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error del servidor vLLM: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando la solicitud: {str(e)}"
        )

@app.get("/stats", tags=["Stats"])
async def get_stats():
    """
    Obtener estadísticas del servidor (futuro)
    """
    return {
        "message": "Stats endpoint - Por implementar",
        "timestamp": datetime.now()
    }

# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn  # ← AGREGAR ESTA LÍNEA
    
    uvicorn.run(
        app,  # Referencia directa al objeto app
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
