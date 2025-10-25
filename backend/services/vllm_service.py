"""
Servicio para comunicación con vLLM
"""
import httpx
import time
from typing import List, Dict, Optional
from config import settings
from models import ChatMessage

class VLLMService:
    """Servicio para interactuar con el servidor vLLM"""
    
    def __init__(self):
        self.api_url = settings.VLLM_API_URL
        self.model_name = settings.VLLM_MODEL_NAME
        self.timeout = settings.VLLM_TIMEOUT
    
    async def check_health(self) -> bool:
        """Verificar si el servidor vLLM está disponible"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.api_url}/health")
                return response.status_code == 200
        except Exception:
            return False
    
    async def get_models(self) -> Dict:
        """Obtener lista de modelos disponibles"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.api_url}/v1/models")
            response.raise_for_status()
            return response.json()
    
    def _build_messages(
        self, 
        user_message: str, 
        conversation_history: Optional[List[ChatMessage]] = None
    ) -> List[Dict[str, str]]:
        """Construir array de mensajes para vLLM"""
        messages = []
        
        # Agregar system prompt
        messages.append({
            "role": "system",
            "content": settings.SYSTEM_PROMPT
        })
        
        # Agregar historial de conversación si existe
        if conversation_history:
            for msg in conversation_history[-6:]:  # Últimos 6 mensajes (3 turnos)
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Agregar mensaje actual del usuario
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    async def chat_completion(
        self,
        message: str,
        conversation_history: Optional[List[ChatMessage]] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
        stream: bool = False
    ) -> Dict:
        """
        Generar respuesta usando Chat Completions API
        
        Returns:
            Dict con response, usage stats y timing
        """
        messages = self._build_messages(message, conversation_history)
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream
        }
        
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.api_url}/v1/chat/completions",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
        
        elapsed_time = time.time() - start_time
        
        # Extraer información relevante
        return {
            "response": result["choices"][0]["message"]["content"].strip(),
            "model": result["model"],
            "usage": result.get("usage", {}),
            "latency_seconds": round(elapsed_time, 2)
        }
    
    async def text_completion(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        stop: Optional[List[str]] = None
    ) -> Dict:
        """
        Generar respuesta usando Text Completions API (alternativa)
        """
        if stop is None:
            stop = ["Usuario:", "\n\n"]
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": stop,
            "stream": False
        }
        
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.api_url}/v1/completions",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
        
        elapsed_time = time.time() - start_time
        
        return {
            "response": result["choices"][0]["text"].strip(),
            "model": result["model"],
            "usage": result.get("usage", {}),
            "latency_seconds": round(elapsed_time, 2)
        }

# Instancia global del servicio
vllm_service = VLLMService()
