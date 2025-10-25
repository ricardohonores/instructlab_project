# InstructLab Project Guide - Guía del Proyecto InstructLab

**[🇬🇧 English](#english-version)** | **[🇪🇸 Español](#versión-en-español)**

---

<a name="english-version"></a>
# CLAUDE.md - InstructLab Project Guide

## Project Overview

This is an **AI Educational Chatbot** built with the **InstructLab** framework. The project integrates:

- **InstructLab Taxonomy** - A community-driven taxonomy of knowledge and skills for fine-tuning AI models
- **vLLM Server** - High-performance language model inference service with GPU support
- **FastAPI Backend** - REST API to handle chat requests and model interactions
- **Nginx Frontend** - Web interface for interactive chatting with the AI model

The project is **containerized with Docker Compose** for easy deployment with proper orchestration of multiple services.

---

## Project Structure

```
instructlab_project/
├── backend/                    # FastAPI API
│   ├── app.py                 # Main application with endpoints
│   ├── config.py              # Configuration and environment variables
│   ├── models.py              # Pydantic validation models
│   ├── services/
│   │   └── vllm_service.py   # Service layer for vLLM
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Container definition
│
├── frontend/                  # Nginx web interface
│   ├── index.html            # Interactive chat UI (656 lines)
│   ├── nginx.conf            # Reverse proxy configuration
│   └── Dockerfile            # Nginx Alpine container
│
├── vllm/                      # vLLM inference service
│   └── Dockerfile            # vLLM container with GPU
│
├── y/                         # InstructLab Taxonomy
│   ├── foundational_skills/  # Basic skills
│   ├── compositional_skills/ # Complex skills
│   ├── knowledge/            # Specific knowledge
│   └── docs/                 # Contribution guides
│
├── models/                    # Fine-tuned models
│   └── samples_0/            # InstructLab fine-tuned model
│
├── scripts/                   # Utility scripts
├── logs/                      # Log files
│
├── docker-compose.yml         # Service orchestration
├── .env                       # Environment variables
│
├── test_backend.py           # Backend endpoint tests
├── test_vllm.py              # Basic vLLM tests
├── test_vllm_chat.py         # Chat completions tests
├── test_vllm_fixed.py        # Tests with error handling
├── test_vllm_complete.py     # Text completions tests
│
├── convert_to_safetensors.py # Model format conversion
└── vllm_server.py            # Standalone vLLM server
```

---

## Main Components

### 1. Backend (FastAPI)

**Location:** `backend/`

**Purpose:** REST API service that:
- Handles chat requests from the frontend
- Communicates with vLLM server for inference
- Manages conversation history and context
- Implements health checks and monitoring

**Main Endpoints:**
```
GET  /              - API information
GET  /health        - Health check (backend + vLLM)
GET  /models        - List of available models
POST /chat          - Main chat endpoint
GET  /stats         - Statistics (placeholder)
```

**Key Dependencies:**
```
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
httpx>=0.27.0
pydantic>=2.11.7
pydantic-settings>=2.7.0
python-dotenv>=1.0.0
```

**Configuration (config.py):**
```python
APP_NAME = "Educational Chatbot API"
APP_VERSION = "1.0.0"
HOST = "0.0.0.0"
PORT = 8000
VLLM_API_URL = "http://localhost:8080"
DEFAULT_MAX_TOKENS = 500
DEFAULT_TEMPERATURE = 0.7
SYSTEM_PROMPT = "You are an expert assistant in AI applied to education..."
```

### 2. vLLM Service

**Location:** `vllm/`

**Purpose:** High-performance LLM inference server

**Configuration:**
- Uses vLLM image compatible with OpenAI
- GPU accelerated (CUDA_VISIBLE_DEVICES=0)
- Serves models from `/models/samples_0`
- Supports up to 4096 context tokens
- 85% GPU memory utilization
- OpenAI-compatible API (/v1/chat/completions, /v1/completions)

**Features:**
- FLASHINFER backend for attention optimization
- Automatic health checks
- Automatic restart on failure

### 3. Frontend (Nginx + HTML/JavaScript)

**Location:** `frontend/`

**Purpose:** Web interface for chatbot interaction

**Features:**
- Responsive UI with purple gradient theme
- Real-time connection status monitoring
- Conversation history management
- Streaming response support
- Auto-resizing textarea
- Token usage and latency display
- Health check every 30 seconds
- Proxy routing: `/api/*` → backend endpoints

### 4. InstructLab Taxonomy (`y/` Directory)

**Location:** `y/`

**Purpose:** Community-driven taxonomy of knowledge and skills for model fine-tuning

**Structure:**
```
y/
├── foundational_skills/        # Basic reasoning, logic, mathematics
│   └── reasoning/
│       ├── mathematical_reasoning/
│       ├── logical_reasoning/
│       ├── common_sense_reasoning/
│       ├── theory_of_mind/
│       └── ... (16 skill categories)
│
├── compositional_skills/       # Complex domain-specific skills
│   ├── linguistics/
│   ├── arts/
│   ├── engineering/
│   ├── technology/
│   └── science/
│
├── knowledge/                  # Domain-specific knowledge
│   ├── science/
│   │   └── animals/
│   │       └── birds/
│   ├── arts/
│   │   └── music/
│   ├── mathematics/
│   └── technology/
│
└── docs/                       # Contribution guides
    ├── KNOWLEDGE_GUIDE.md
    └── SKILLS_GUIDE.md
```

**Data Format (YAML - qna.yaml):**
```yaml
created_by: ibm
version: 3
domain: animals
task_description: "Teach the model about mathematical operations."
seed_examples:
  - question: "Which is heavier?"
    answer: "A kilogram of feathers is heavier..."
  - question: "..."
    answer: "..."
```

**Statistics:**
- 16+ seed examples from qna.yaml files
- 89+ subdirectories organizing knowledge/skills
- Based on Dewey Decimal Classification (DDC)

### 5. Models

**Location:** `models/`

**Current Model:**
- `samples_0/` - InstructLab fine-tuned model
- Format: HuggingFace standard with pytorch_model.bin
- Helper script: `convert_to_safetensors.py` for format conversion

---

## How the System Works

### Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Network                    │
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

### Request Flow

1. **User Interaction:**
   - User opens browser → Nginx Frontend loads (port 80)
   - User types message in web UI

2. **Frontend Processing:**
   - JavaScript captures input
   - Sends POST request to `/api/chat`
   - Nginx proxy rewrites to `http://chatbot-backend:8000/chat`

3. **Backend Processing:**
   - FastAPI receives ChatRequest (message, history, parameters)
   - Creates system prompt + history + user message
   - Validates input with Pydantic models
   - Calls vLLM service

4. **vLLM Inference:**
   - Backend sends JSON payload to vLLM OpenAI API
   - vLLM loads model from `/models/samples_0`
   - GPU accelerates inference (FLASHINFER attention backend)
   - Returns response with token usage and timing

5. **Response Chain:**
   - Backend calculates latency
   - Wraps response in ChatResponse model
   - Returns JSON: { response, model, tokens_used, latency_seconds, timestamp }
   - Frontend displays response and updates history

### Interdependencies

- vLLM must be healthy before Backend starts (depends_on with health check)
- Backend must be healthy before Frontend starts
- All services on same docker network for internal communication
- Health checks every 30 seconds to monitor service status

---

## Technology Stack

### Backend
- **Language:** Python 3.11
- **Framework:** FastAPI (async REST API)
- **Web Server:** Uvicorn (ASGI server)
- **Validation:** Pydantic v2.11.7
- **HTTP Client:** httpx (async for vLLM calls)
- **Configuration:** pydantic-settings, python-dotenv

### LLM Inference
- **vLLM:** Open-source library for serving LLMs
- **Backend:** OpenAI-compatible API
- **GPU Support:** NVIDIA CUDA with FLASHINFER optimization
- **Model Format:** HuggingFace transformers

### Frontend
- **Web Server:** Nginx (Alpine Linux)
- **UI:** HTML5 + vanilla JavaScript
- **Styles:** CSS3 with gradients and animations
- **Communication:** Async Fetch API with JSON

### Containerization
- **Docker:** Container orchestration
- **Docker Compose:** Multi-container deployment
- **Images:**
  - Backend: python:3.11-slim
  - vLLM: vllm/vllm-openai:latest
  - Frontend: nginx:alpine

### Data and ML
- **InstructLab:** Framework for LLM fine-tuning with taxonomy-based data
- **Data Format:** YAML (qna.yaml for Q&A pairs)
- **Fine-tuning Method:** LAB (Large-Scale Alignment for ChatBots)
- **Model Type:** Transformer-based LLM with LoRA adapters

---

## How to Work with the Project

### Prerequisites

1. **Docker and Docker Compose** installed
2. **NVIDIA GPU** with CUDA drivers (for vLLM)
3. **Model downloaded** in `models/samples_0/`

### Quick Start

1. **Clone/Navigate to project:**
   ```bash
   cd /home/honores/instructlab_project
   ```

2. **Check environment variables (.env):**
   ```bash
   COMPOSE_PROJECT_NAME=chatbot-educativo
   VLLM_PORT=8080
   VLLM_GPU_MEMORY=0.85
   VLLM_MAX_MODEL_LEN=4096
   BACKEND_PORT=8000
   FRONTEND_PORT=80
   MODEL_PATH=./models/samples_0
   ```

3. **Start all services:**
   ```bash
   docker-compose up -d
   ```

4. **Verify services are running:**
   ```bash
   docker-compose ps
   ```

5. **View logs:**
   ```bash
   # All services
   docker-compose logs -f

   # Specific service
   docker-compose logs -f chatbot-backend
   docker-compose logs -f vllm-server
   docker-compose logs -f chatbot-frontend
   ```

6. **Access the application:**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - vLLM API: http://localhost:8080
   - Health Check: http://localhost:8000/health

### Stop Services

```bash
# Stop without removing containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

### Development and Testing

#### Run Tests

```bash
# Test backend endpoints
python test_backend.py

# Test vLLM chat completions
python test_vllm_chat.py

# Test vLLM with improved error handling
python test_vllm_fixed.py

# Test text completions
python test_vllm_complete.py
```

#### Modify Backend

1. Edit files in `backend/`
2. Rebuild container:
   ```bash
   docker-compose up -d --build chatbot-backend
   ```

#### Modify Frontend

1. Edit `frontend/index.html` or `frontend/nginx.conf`
2. Rebuild container:
   ```bash
   docker-compose up -d --build chatbot-frontend
   ```

#### Development with Auto-reload

For active backend development:

```bash
# Stop backend container
docker-compose stop chatbot-backend

# Run locally with auto-reload
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Working with Taxonomy

#### Add New Knowledge

1. Navigate to appropriate directory:
   ```bash
   cd y/knowledge/[domain]/
   ```

2. Create subdirectory for your topic:
   ```bash
   mkdir my_topic
   cd my_topic
   ```

3. Create `qna.yaml` file:
   ```yaml
   created_by: your_name
   version: 3
   domain: domain_name
   task_description: "Description of what this knowledge teaches."
   seed_examples:
     - question: "Question 1?"
       answer: "Detailed answer..."
     - question: "Question 2?"
       answer: "Detailed answer..."
   ```

4. Add at least 5 question-answer pairs

#### Add New Skill

1. Navigate to:
   - `y/foundational_skills/` for basic skills
   - `y/compositional_skills/` for complex skills

2. Create appropriate directory structure

3. Create `qna.yaml` with skill examples

4. Consult `y/docs/SKILLS_GUIDE.md` for best practices

#### Re-train Model

After adding data to taxonomy:

```bash
# Generate synthetic data (requires InstructLab CLI)
ilab data generate

# Train model
ilab model train

# Convert to vLLM format if necessary
python convert_to_safetensors.py
```

### Advanced Configuration

#### Adjust vLLM Parameters

Edit `docker-compose.yml`:

```yaml
vllm-server:
  command: >
    --model /models/samples_0
    --gpu-memory-utilization 0.9    # Increase GPU usage
    --max-model-len 8192            # Increase context
    --dtype float16                 # Change precision
    --tensor-parallel-size 2        # Multi-GPU
```

#### Change Model

1. Place new model in `models/`
2. Update `MODEL_PATH` in `.env`
3. Restart services:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

#### Configure CORS

Edit `backend/config.py`:

```python
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "https://my-domain.com",  # Add your domain
]
```

### Monitoring

#### Health Checks

```bash
# Check backend health
curl http://localhost:8000/health

# Check vLLM health
curl http://localhost:8080/health

# View available models
curl http://localhost:8000/models
```

#### Metrics

```bash
# View Docker resource usage
docker stats

# View logs in real-time
docker-compose logs -f --tail=100
```

### Troubleshooting

#### vLLM doesn't start

1. Verify GPU available:
   ```bash
   nvidia-smi
   ```

2. Verify sufficient GPU memory (model requires ~8GB)

3. Check logs:
   ```bash
   docker-compose logs vllm-server
   ```

#### Backend can't connect to vLLM

1. Verify vLLM is healthy:
   ```bash
   docker-compose ps
   ```

2. Verify network connectivity:
   ```bash
   docker-compose exec chatbot-backend ping vllm-server
   ```

3. Check `VLLM_API_URL` variable in `backend/config.py`

#### Frontend shows connection error

1. Verify backend is running
2. Check proxy configuration in `frontend/nginx.conf`
3. View Nginx logs:
   ```bash
   docker-compose logs chatbot-frontend
   ```

#### Model doesn't load

1. Verify model exists in `models/samples_0/`
2. Check read permissions
3. Convert to safetensors if necessary:
   ```bash
   python convert_to_safetensors.py
   ```

---

## Utility Scripts

### convert_to_safetensors.py

Converts PyTorch models to SafeTensors format for vLLM:

```bash
python convert_to_safetensors.py
```

### vllm_server.py

Starts standalone vLLM server (without Docker):

```bash
python vllm_server.py
```

---

## Ports and Access

### Exposed Ports

- **80** - Frontend (web interface)
- **8000** - Backend API
- **8080** - vLLM API

### Access URLs

- **Web Application:** http://localhost
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **vLLM OpenAI API:** http://localhost:8080/v1/

---

## API Endpoints

### GET /

Basic API information.

**Response:**
```json
{
  "message": "Educational Chatbot API",
  "version": "1.0.0",
  "vllm_status": "connected"
}
```

### GET /health

Backend and vLLM health check.

**Response:**
```json
{
  "status": "healthy",
  "backend": "ok",
  "vllm": "ok",
  "timestamp": "2024-10-24T15:30:00"
}
```

### GET /models

List of available models.

**Response:**
```json
{
  "models": ["/models/samples_0"],
  "active_model": "/models/samples_0"
}
```

### POST /chat

Main chat endpoint.

**Request Body:**
```json
{
  "message": "What is machine learning?",
  "conversation_history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hello! How can I help you?"}
  ],
  "max_tokens": 500,
  "temperature": 0.7,
  "stream": false
}
```

**Response:**
```json
{
  "response": "Machine learning is...",
  "model": "/models/samples_0",
  "tokens_used": 145,
  "prompt_tokens": 42,
  "completion_tokens": 103,
  "latency_seconds": 2.34,
  "timestamp": "2024-10-24T15:30:00.123456"
}
```

---

## Best Practices

### Security

1. **Don't expose vLLM directly** - Only accessible through backend
2. **Use HTTPS in production** - Configure SSL certificates
3. **Limit CORS** - Only trusted origins in `config.py`
4. **Rate limiting** - Implement rate limits for /chat endpoint
5. **Authentication** - Add JWT or API keys for production

### Performance

1. **Adjust GPU memory** - Balance between model size and batch size
2. **Cache responses** - For frequent questions
3. **Use streaming** - For long responses (set `stream: true`)
4. **Monitor resources** - Use `docker stats` regularly
5. **Optimize context length** - Don't use more than necessary

### Maintenance

1. **Rotating logs** - Configure logrotate to avoid filling disk
2. **Model backups** - Keep copies of fine-tuned models
3. **Update dependencies** - Regularly review and update
4. **Monitor health** - Setup alerts for down services
5. **Document changes** - Maintain changelog of taxonomy modifications

---

## Additional Resources

### Documentation

- **InstructLab:** https://github.com/instructlab/instructlab
- **vLLM:** https://docs.vllm.ai/
- **FastAPI:** https://fastapi.tiangolo.com/
- **Docker Compose:** https://docs.docker.com/compose/

### Project Guides

- `y/docs/KNOWLEDGE_GUIDE.md` - How to contribute knowledge
- `y/docs/SKILLS_GUIDE.md` - How to contribute skills
- `y/README.md` - Taxonomy overview

### Support

For issues or questions:
1. Review logs: `docker-compose logs -f`
2. Check health checks
3. Consult InstructLab documentation
4. Review issues in project repository

---

## Complete Flow Example

### Add Knowledge and Use in Chat

1. **Create new knowledge about Python:**

```bash
cd y/knowledge/technology/programming/
mkdir python_basics
cd python_basics
```

2. **Create qna.yaml:**

```yaml
created_by: developer
version: 3
domain: programming
task_description: "Teach basic Python concepts."
seed_examples:
  - question: "What is a list in Python?"
    answer: "A list in Python is a data structure..."
  - question: "How do I define a function in Python?"
    answer: "In Python you define a function using def..."
  - question: "What are comprehensions in Python?"
    answer: "Comprehensions are a concise way to..."
```

3. **Re-train model (outside Docker):**

```bash
# From project root directory
ilab data generate --taxonomy-path ./y
ilab model train --data-path generated_data
```

4. **Update model in Docker:**

```bash
# Copy trained model to models/
cp -r ~/.local/share/instructlab/checkpoints/hf_format/samples_1 ./models/

# Update .env
echo "MODEL_PATH=./models/samples_1" >> .env

# Restart services
docker-compose down
docker-compose up -d
```

5. **Test in application:**

Open http://localhost and ask: "What is a list in Python?"

The model should now respond using the added knowledge.

---

## Production Configuration

### Additional Environment Variables

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

### Reverse Proxy (External Nginx)

```nginx
# /etc/nginx/sites-available/chatbot
upstream backend {
    server localhost:8000;
}

server {
    listen 443 ssl http2;
    server_name chatbot.mydomain.com;

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

## Final Notes

This project demonstrates:

1. ✅ **Modern architecture** - Microservices with Docker
2. ✅ **State-of-the-art AI** - vLLM + InstructLab
3. ✅ **Scalability** - Easy to scale horizontally
4. ✅ **Maintainability** - Clean and well-documented code
5. ✅ **Community-driven** - Collaborative taxonomy
6. ✅ **Production-ready** - Health checks, error handling, logging

To get started, simply run:

```bash
docker-compose up -d
```

And open http://localhost in your browser.

---

**Last update:** 2024-10-24
**Version:** 1.0.0
**Author:** InstructLab System

**[🇪🇸 Ver versión en español](#versión-en-español)**

---
---

<a name="versión-en-español"></a>
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

**[🇬🇧 View English version](#english-version)**
