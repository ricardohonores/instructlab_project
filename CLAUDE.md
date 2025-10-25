# CLAUDE.md - Guía del Proyecto InstructLab

## Descripción General del Proyecto

Este es un **Chatbot Educativo de IA** construido con el framework **InstructLab**. El proyecto integra:

- **Taxonomía InstructLab** - Una taxonomía de conocimientos y habilidades impulsada por la comunidad para ajuste fino de modelos de IA
- **Servidor vLLM** - Servicio de inferencia de modelos de lenguaje de alto rendimiento con soporte GPU
- **Backend FastAPI** - API REST para manejar solicitudes de chat e interacciones con el modelo
- **Frontend Nginx** - Interfaz web para chatear interactivamente con el modelo de IA

El proyecto está **containerizado con Docker Compose** para facilitar el despliegue con orquestación adecuada de múltiples servicios.

---

## Estructura del Proyecto

```
instructlab_project/
├── backend/                    # API FastAPI
│   ├── app.py                 # Aplicación principal con endpoints
│   ├── config.py              # Configuración y variables de entorno
│   ├── models.py              # Modelos de validación Pydantic
│   ├── services/
│   │   └── vllm_service.py   # Capa de servicio para vLLM
│   ├── requirements.txt       # Dependencias Python
│   └── Dockerfile            # Definición del contenedor
│
├── frontend/                  # Interfaz web Nginx
│   ├── index.html            # UI de chat interactiva (656 líneas)
│   ├── nginx.conf            # Configuración proxy reverso
│   └── Dockerfile            # Contenedor Nginx Alpine
│
├── vllm/                      # Servicio de inferencia vLLM
│   └── Dockerfile            # Contenedor vLLM con GPU
│
├── y/                         # Taxonomía InstructLab
│   ├── foundational_skills/  # Habilidades básicas
│   ├── compositional_skills/ # Habilidades complejas
│   ├── knowledge/            # Conocimiento específico
│   └── docs/                 # Guías de contribución
│
├── models/                    # Modelos ajustados
│   └── samples_0/            # Modelo InstructLab fine-tuned
│
├── scripts/                   # Scripts de utilidad
├── logs/                      # Archivos de registro
│
├── docker-compose.yml         # Orquestación de servicios
├── .env                       # Variables de entorno
│
├── test_backend.py           # Tests de endpoints backend
├── test_vllm.py              # Tests básicos vLLM
├── test_vllm_chat.py         # Tests chat completions
├── test_vllm_fixed.py        # Tests con manejo de errores
├── test_vllm_complete.py     # Tests text completions
│
├── convert_to_safetensors.py # Conversión de formato modelo
└── vllm_server.py            # Servidor vLLM standalone
```

---

## Componentes Principales

### 1. Backend (FastAPI)

**Ubicación:** `backend/`

**Propósito:** Servicio API REST que:
- Maneja solicitudes de chat del frontend
- Se comunica con el servidor vLLM para inferencia
- Gestiona historial de conversación y contexto
- Implementa health checks y monitoreo

**Endpoints Principales:**
```
GET  /              - Información de la API
GET  /health        - Health check (backend + vLLM)
GET  /models        - Lista de modelos disponibles
POST /chat          - Endpoint principal de chat
GET  /stats         - Estadísticas (placeholder)
```

**Dependencias Clave:**
```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
httpx>=0.27.0
pydantic>=2.11.7
pydantic-settings>=2.7.0
python-dotenv>=1.0.0
```

**Configuración (config.py):**
```python
APP_NAME = "Chatbot Educativo API"
APP_VERSION = "1.0.0"
HOST = "0.0.0.0"
PORT = 8000
VLLM_API_URL = "http://localhost:8080"
DEFAULT_MAX_TOKENS = 500
DEFAULT_TEMPERATURE = 0.7
SYSTEM_PROMPT = "Eres un asistente experto en IA aplicada a la educación..."
```

### 2. Servicio vLLM

**Ubicación:** `vllm/`

**Propósito:** Servidor de inferencia de LLM de alto rendimiento

**Configuración:**
- Usa imagen vLLM compatible con OpenAI
- Acelerado por GPU (CUDA_VISIBLE_DEVICES=0)
- Sirve modelos desde `/models/samples_0`
- Soporta hasta 4096 tokens de contexto
- 85% de utilización de memoria GPU
- API compatible con OpenAI (/v1/chat/completions, /v1/completions)

**Características:**
- FLASHINFER backend para optimización de atención
- Health checks automáticos
- Reinicio automático en caso de falla

### 3. Frontend (Nginx + HTML/JavaScript)

**Ubicación:** `frontend/`

**Propósito:** Interfaz web para interacción con el chatbot

**Características:**
- UI responsive con tema morado gradiente
- Monitoreo de estado de conexión en tiempo real
- Gestión de historial de conversación
- Soporte para respuestas streaming
- Textarea con auto-redimensionamiento
- Display de uso de tokens y latencia
- Health check cada 30 segundos
- Proxy routing: `/api/*` → endpoints backend

### 4. Taxonomía InstructLab (Directorio `y/`)

**Ubicación:** `y/`

**Propósito:** Taxonomía de conocimientos y habilidades impulsada por la comunidad para ajuste fino del modelo

**Estructura:**
```
y/
├── foundational_skills/        # Razonamiento básico, lógica, matemáticas
│   └── reasoning/
│       ├── mathematical_reasoning/
│       ├── logical_reasoning/
│       ├── common_sense_reasoning/
│       ├── theory_of_mind/
│       └── ... (16 categorías de habilidades)
│
├── compositional_skills/       # Habilidades complejas específicas de dominio
│   ├── linguistics/
│   ├── arts/
│   ├── engineering/
│   ├── technology/
│   └── science/
│
├── knowledge/                  # Conocimiento específico de dominio
│   ├── science/
│   │   └── animals/
│   │       └── birds/
│   ├── arts/
│   │   └── music/
│   ├── mathematics/
│   └── technology/
│
└── docs/                       # Guías de contribución
    ├── KNOWLEDGE_GUIDE.md
    └── SKILLS_GUIDE.md
```

**Formato de Datos (YAML - qna.yaml):**
```yaml
created_by: ibm
version: 3
domain: animals
task_description: "Enseñar al modelo sobre operaciones matemáticas."
seed_examples:
  - question: "¿Qué es más pesado?"
    answer: "Un kilo de plumas es más pesado..."
  - question: "..."
    answer: "..."
```

**Estadísticas:**
- 16+ ejemplos semilla de archivos qna.yaml
- 89+ subdirectorios organizando conocimientos/habilidades
- Basado en Clasificación Decimal Dewey (DDC)

### 5. Modelos

**Ubicación:** `models/`

**Modelo Actual:**
- `samples_0/` - Modelo InstructLab fine-tuned
- Formato: HuggingFace estándar con pytorch_model.bin
- Script helper: `convert_to_safetensors.py` para conversión de formato

---

## Cómo Funciona el Sistema

### Arquitectura de Red

```
┌─────────────────────────────────────────────────────────────┐
│                    Red Docker Compose                        │
│              chatbot-network (bridge driver)                 │
└─────────────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ┌────▼─────┐         ┌─────▼────┐         ┌──────▼──────┐
   │ Frontend  │         │ Backend   │         │  vLLM       │
   │ (Nginx)   │────────▶│ (FastAPI) │────────▶│ (GPU)       │
   │ Port: 80  │         │Port: 8000 │         │Port: 8000   │
   └──────────┘         └──────────┘         └─────────────┘
```

### Flujo de Solicitud

1. **Interacción del Usuario:**
   - Usuario abre navegador → Frontend Nginx carga (puerto 80)
   - Usuario escribe mensaje en UI web

2. **Procesamiento Frontend:**
   - JavaScript captura entrada
   - Envía POST request a `/api/chat`
   - Nginx proxy reescribe a `http://chatbot-backend:8000/chat`

3. **Procesamiento Backend:**
   - FastAPI recibe ChatRequest (mensaje, historial, parámetros)
   - Crea prompt del sistema + historial + mensaje del usuario
   - Valida entrada con modelos Pydantic
   - Llama al servicio vLLM

4. **Inferencia vLLM:**
   - Backend envía payload JSON a API OpenAI de vLLM
   - vLLM carga modelo desde `/models/samples_0`
   - GPU acelera inferencia (backend de atención FLASHINFER)
   - Retorna respuesta con uso de tokens y timing

5. **Cadena de Respuesta:**
   - Backend calcula latencia
   - Envuelve respuesta en modelo ChatResponse
   - Retorna JSON: { response, model, tokens_used, latency_seconds, timestamp }
   - Frontend muestra respuesta y actualiza historial

### Interdependencias

- vLLM debe estar saludable antes de que Backend inicie (depends_on con health check)
- Backend debe estar saludable antes de que Frontend inicie
- Todos los servicios en la misma red docker para comunicación interna
- Health checks cada 30 segundos para monitorear estado de servicios

---

## Stack Tecnológico

### Backend
- **Lenguaje:** Python 3.11
- **Framework:** FastAPI (async REST API)
- **Servidor Web:** Uvicorn (servidor ASGI)
- **Validación:** Pydantic v2.11.7
- **Cliente HTTP:** httpx (async para llamadas vLLM)
- **Configuración:** pydantic-settings, python-dotenv

### Inferencia LLM
- **vLLM:** Librería open-source para servir LLMs
- **Backend:** API compatible con OpenAI
- **Soporte GPU:** NVIDIA CUDA con optimización FLASHINFER
- **Formato Modelo:** HuggingFace transformers

### Frontend
- **Servidor Web:** Nginx (Alpine Linux)
- **UI:** HTML5 + JavaScript vanilla
- **Estilos:** CSS3 con gradientes y animaciones
- **Comunicación:** Fetch API async con JSON

### Containerización
- **Docker:** Orquestación de contenedores
- **Docker Compose:** Despliegue multi-contenedor
- **Imágenes:**
  - Backend: python:3.11-slim
  - vLLM: vllm/vllm-openai:latest
  - Frontend: nginx:alpine

### Datos y ML
- **InstructLab:** Framework para ajuste fino de LLMs con datos basados en taxonomía
- **Formato Datos:** YAML (qna.yaml para pares Q&A)
- **Método Fine-tuning:** LAB (Large-Scale Alignment for ChatBots)
- **Tipo Modelo:** LLM basado en Transformers con adaptadores LoRA

---

## Cómo Trabajar con el Proyecto

### Prerequisitos

1. **Docker y Docker Compose** instalados
2. **GPU NVIDIA** con drivers CUDA (para vLLM)
3. **Modelo descargado** en `models/samples_0/`

### Inicio Rápido

1. **Clonar/Navegar al proyecto:**
   ```bash
   cd /home/honores/instructlab_project
   ```

2. **Verificar variables de entorno (.env):**
   ```bash
   COMPOSE_PROJECT_NAME=chatbot-educativo
   VLLM_PORT=8080
   VLLM_GPU_MEMORY=0.85
   VLLM_MAX_MODEL_LEN=4096
   BACKEND_PORT=8000
   FRONTEND_PORT=80
   MODEL_PATH=./models/samples_0
   ```

3. **Iniciar todos los servicios:**
   ```bash
   docker-compose up -d
   ```

4. **Verificar que los servicios estén corriendo:**
   ```bash
   docker-compose ps
   ```

5. **Ver logs:**
   ```bash
   # Todos los servicios
   docker-compose logs -f

   # Servicio específico
   docker-compose logs -f chatbot-backend
   docker-compose logs -f vllm-server
   docker-compose logs -f chatbot-frontend
   ```

6. **Acceder a la aplicación:**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - vLLM API: http://localhost:8080
   - Health Check: http://localhost:8000/health

### Detener Servicios

```bash
# Detener sin eliminar contenedores
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar contenedores + volúmenes
docker-compose down -v
```

### Desarrollo y Testing

#### Ejecutar Tests

```bash
# Test backend endpoints
python test_backend.py

# Test vLLM chat completions
python test_vllm_chat.py

# Test vLLM con manejo de errores mejorado
python test_vllm_fixed.py

# Test text completions
python test_vllm_complete.py
```

#### Modificar Backend

1. Editar archivos en `backend/`
2. Reconstruir contenedor:
   ```bash
   docker-compose up -d --build chatbot-backend
   ```

#### Modificar Frontend

1. Editar `frontend/index.html` o `frontend/nginx.conf`
2. Reconstruir contenedor:
   ```bash
   docker-compose up -d --build chatbot-frontend
   ```

#### Desarrollo con Auto-reload

Para desarrollo activo del backend:

```bash
# Detener contenedor backend
docker-compose stop chatbot-backend

# Ejecutar localmente con auto-reload
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Trabajar con la Taxonomía

#### Agregar Nuevo Conocimiento

1. Navegar a directorio apropiado:
   ```bash
   cd y/knowledge/[dominio]/
   ```

2. Crear subdirectorio para tu tema:
   ```bash
   mkdir mi_tema
   cd mi_tema
   ```

3. Crear archivo `qna.yaml`:
   ```yaml
   created_by: tu_nombre
   version: 3
   domain: nombre_dominio
   task_description: "Descripción de qué enseña este conocimiento."
   seed_examples:
     - question: "¿Pregunta 1?"
       answer: "Respuesta detallada..."
     - question: "¿Pregunta 2?"
       answer: "Respuesta detallada..."
   ```

4. Agregar al menos 5 pares de preguntas-respuestas

#### Agregar Nueva Habilidad

1. Navegar a:
   - `y/foundational_skills/` para habilidades básicas
   - `y/compositional_skills/` para habilidades complejas

2. Crear estructura de directorios apropiada

3. Crear `qna.yaml` con ejemplos de la habilidad

4. Consultar `y/docs/SKILLS_GUIDE.md` para mejores prácticas

#### Re-entrenar Modelo

Después de agregar datos a la taxonomía:

```bash
# Generar datos sintéticos (requiere InstructLab CLI)
ilab data generate

# Entrenar modelo
ilab model train

# Convertir a formato vLLM si es necesario
python convert_to_safetensors.py
```

### Configuración Avanzada

#### Ajustar Parámetros vLLM

Editar `docker-compose.yml`:

```yaml
vllm-server:
  command: >
    --model /models/samples_0
    --gpu-memory-utilization 0.9    # Aumentar uso de GPU
    --max-model-len 8192            # Aumentar contexto
    --dtype float16                 # Cambiar precisión
    --tensor-parallel-size 2        # Multi-GPU
```

#### Cambiar Modelo

1. Colocar nuevo modelo en `models/`
2. Actualizar `MODEL_PATH` en `.env`
3. Reiniciar servicios:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

#### Configurar CORS

Editar `backend/config.py`:

```python
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "https://mi-dominio.com",  # Agregar tu dominio
]
```

### Monitoreo

#### Health Checks

```bash
# Check backend health
curl http://localhost:8000/health

# Check vLLM health
curl http://localhost:8080/health

# Ver modelos disponibles
curl http://localhost:8000/models
```

#### Métricas

```bash
# Ver uso de recursos Docker
docker stats

# Ver logs en tiempo real
docker-compose logs -f --tail=100
```

### Troubleshooting

#### vLLM no inicia

1. Verificar GPU disponible:
   ```bash
   nvidia-smi
   ```

2. Verificar memoria GPU suficiente (modelo requiere ~8GB)

3. Verificar logs:
   ```bash
   docker-compose logs vllm-server
   ```

#### Backend no puede conectar a vLLM

1. Verificar que vLLM esté healthy:
   ```bash
   docker-compose ps
   ```

2. Verificar conectividad de red:
   ```bash
   docker-compose exec chatbot-backend ping vllm-server
   ```

3. Verificar variable `VLLM_API_URL` en `backend/config.py`

#### Frontend muestra error de conexión

1. Verificar que backend esté corriendo
2. Verificar configuración de proxy en `frontend/nginx.conf`
3. Ver logs de Nginx:
   ```bash
   docker-compose logs chatbot-frontend
   ```

#### Modelo no carga

1. Verificar que el modelo existe en `models/samples_0/`
2. Verificar permisos de lectura
3. Convertir a safetensors si es necesario:
   ```bash
   python convert_to_safetensors.py
   ```

---

## Scripts de Utilidad

### convert_to_safetensors.py

Convierte modelos PyTorch a formato SafeTensors para vLLM:

```bash
python convert_to_safetensors.py
```

### vllm_server.py

Inicia servidor vLLM standalone (sin Docker):

```bash
python vllm_server.py
```

---

## Puertos y Acceso

### Puertos Expuestos

- **80** - Frontend (interfaz web)
- **8000** - Backend API
- **8080** - vLLM API

### URLs de Acceso

- **Aplicación Web:** http://localhost
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **vLLM OpenAI API:** http://localhost:8080/v1/

---

## Endpoints de la API

### GET /

Información básica de la API.

**Respuesta:**
```json
{
  "message": "Chatbot Educativo API",
  "version": "1.0.0",
  "vllm_status": "connected"
}
```

### GET /health

Health check del backend y vLLM.

**Respuesta:**
```json
{
  "status": "healthy",
  "backend": "ok",
  "vllm": "ok",
  "timestamp": "2024-10-24T15:30:00"
}
```

### GET /models

Lista de modelos disponibles.

**Respuesta:**
```json
{
  "models": ["/models/samples_0"],
  "active_model": "/models/samples_0"
}
```

### POST /chat

Endpoint principal de chat.

**Request Body:**
```json
{
  "message": "¿Qué es el aprendizaje automático?",
  "conversation_history": [
    {"role": "user", "content": "Hola"},
    {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte?"}
  ],
  "max_tokens": 500,
  "temperature": 0.7,
  "stream": false
}
```

**Response:**
```json
{
  "response": "El aprendizaje automático es...",
  "model": "/models/samples_0",
  "tokens_used": 145,
  "prompt_tokens": 42,
  "completion_tokens": 103,
  "latency_seconds": 2.34,
  "timestamp": "2024-10-24T15:30:00.123456"
}
```

---

## Mejores Prácticas

### Seguridad

1. **No exponer vLLM directamente** - Solo accesible a través del backend
2. **Usar HTTPS en producción** - Configurar certificados SSL
3. **Limitar CORS** - Solo orígenes confiables en `config.py`
4. **Rate limiting** - Implementar límites de tasa para /chat endpoint
5. **Autenticación** - Agregar JWT o API keys para producción

### Performance

1. **Ajustar GPU memory** - Balancear entre tamaño de modelo y batch size
2. **Cachear respuestas** - Para preguntas frecuentes
3. **Usar streaming** - Para respuestas largas (set `stream: true`)
4. **Monitorear recursos** - Usar `docker stats` regularmente
5. **Optimizar context length** - No usar más de lo necesario

### Mantenimiento

1. **Logs rotativos** - Configurar logrotate para evitar llenar disco
2. **Backups de modelos** - Mantener copias de modelos fine-tuned
3. **Actualizar dependencias** - Regularmente revisar y actualizar
4. **Monitorear health** - Setup alertas para servicios caídos
5. **Documentar cambios** - Mantener changelog de modificaciones a taxonomía

---

## Recursos Adicionales

### Documentación

- **InstructLab:** https://github.com/instructlab/instructlab
- **vLLM:** https://docs.vllm.ai/
- **FastAPI:** https://fastapi.tiangolo.com/
- **Docker Compose:** https://docs.docker.com/compose/

### Guías del Proyecto

- `y/docs/KNOWLEDGE_GUIDE.md` - Cómo contribuir conocimiento
- `y/docs/SKILLS_GUIDE.md` - Cómo contribuir habilidades
- `y/README.md` - Visión general de la taxonomía

### Soporte

Para problemas o preguntas:
1. Revisar logs: `docker-compose logs -f`
2. Verificar health checks
3. Consultar documentación de InstructLab
4. Revisar issues en repositorio del proyecto

---

## Ejemplo de Flujo Completo

### Agregar Conocimiento y Usar en Chat

1. **Crear nuevo conocimiento sobre Python:**

```bash
cd y/knowledge/technology/programming/
mkdir python_basics
cd python_basics
```

2. **Crear qna.yaml:**

```yaml
created_by: developer
version: 3
domain: programming
task_description: "Enseñar conceptos básicos de Python."
seed_examples:
  - question: "¿Qué es una lista en Python?"
    answer: "Una lista en Python es una estructura de datos..."
  - question: "¿Cómo defino una función en Python?"
    answer: "En Python defines una función usando def..."
  - question: "¿Qué son las comprehensions en Python?"
    answer: "Las comprehensions son una forma concisa de..."
```

3. **Re-entrenar modelo (fuera de Docker):**

```bash
# Desde el directorio raíz del proyecto
ilab data generate --taxonomy-path ./y
ilab model train --data-path generated_data
```

4. **Actualizar modelo en Docker:**

```bash
# Copiar modelo entrenado a models/
cp -r ~/.local/share/instructlab/checkpoints/hf_format/samples_1 ./models/

# Actualizar .env
echo "MODEL_PATH=./models/samples_1" >> .env

# Reiniciar servicios
docker-compose down
docker-compose up -d
```

5. **Probar en la aplicación:**

Abrir http://localhost y preguntar: "¿Qué es una lista en Python?"

El modelo ahora debería responder usando el conocimiento agregado.

---

## Configuración de Producción

### Variables de Entorno Adicionales

```bash
# .env.production
COMPOSE_PROJECT_NAME=chatbot-educativo-prod
DEBUG=false
LOG_LEVEL=warning
WORKERS=4                          # Uvicorn workers
MAX_REQUESTS=1000                  # Rate limiting
ENABLE_HTTPS=true
SSL_CERT_PATH=/etc/ssl/certs/cert.pem
SSL_KEY_PATH=/etc/ssl/private/key.pem
```

### Reverse Proxy (Nginx Externo)

```nginx
# /etc/nginx/sites-available/chatbot
upstream backend {
    server localhost:8000;
}

server {
    listen 443 ssl http2;
    server_name chatbot.midominio.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
    }
}
```

---

## Notas Finales

Este proyecto demuestra:

1. ✅ **Arquitectura moderna** - Microservicios con Docker
2. ✅ **IA de última generación** - vLLM + InstructLab
3. ✅ **Escalabilidad** - Fácil de escalar horizontalmente
4. ✅ **Mantenibilidad** - Código limpio y bien documentado
5. ✅ **Community-driven** - Taxonomía colaborativa
6. ✅ **Production-ready** - Health checks, error handling, logging

Para comenzar a trabajar, simplemente ejecuta:

```bash
docker-compose up -d
```

Y abre http://localhost en tu navegador.

---

**Última actualización:** 2024-10-24
**Versión:** 1.0.0
**Autor:** Sistema InstructLab
