# InstructLab Educational Chatbot

**[🇬🇧 English](#english-version)** | **[🇪🇸 Español](#versión-en-español)**

---

<a name="english-version"></a>
# InstructLab Educational Chatbot

An AI educational chatbot built with the **InstructLab** framework, optimized for high-performance inference with **vLLM** and an interactive web interface.

## Features

- **InstructLab Framework**: Fine-tune LLM models using community-driven knowledge and skills taxonomy
- **vLLM Inference**: High-performance inference server with GPU acceleration and OpenAI-compatible API
- **FastAPI Backend**: Async REST API with Pydantic validation and robust error handling
- **Interactive Web Frontend**: Responsive chat interface with real-time status monitoring
- **Containerized Architecture**: Docker Compose deployment for easy service orchestration
- **Health Monitoring**: Automatic health checks and service restart
- **Extensible Taxonomy**: Dewey Decimal Classification-based system for organizing knowledge

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Frontend   │─────▶│  Backend    │─────▶│    vLLM     │
│   (Nginx)   │      │  (FastAPI)  │      │   (GPU)     │
│   Port: 80  │      │  Port: 8000 │      │ Port: 8000  │
└─────────────┘      └─────────────┘      └─────────────┘
```

**Data Flow:**
1. User interacts with web interface (Nginx)
2. Frontend sends requests to Backend via `/api/*`
3. Backend processes request and calls vLLM for inference
4. vLLM executes model on GPU and returns response
5. Backend formats response with metrics (tokens, latency)
6. Frontend displays response to user

## Prerequisites

- **Docker** and **Docker Compose** (v2.0+)
- **NVIDIA GPU** with CUDA drivers installed (for vLLM)
- **8GB+ RAM** (16GB recommended)
- **Minimum 10GB disk space** (excluding models)
- **Python 3.11+** (for local development)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ricardohonores/instructlab_project.git
cd instructlab_project
```

### 2. Obtain the Model

This project requires a fine-tuned language model with InstructLab. You have several options:

#### Option A: Use a Pre-trained InstructLab Model

```bash
# Install InstructLab CLI
pip install instructlab

# Download InstructLab base model
ilab model download

# The model will download to ~/.local/share/instructlab/models/
# Copy or create symlink to project directory
mkdir -p models
ln -s ~/.local/share/instructlab/models/merlinite-7b-lab-Q4_K_M.gguf models/samples_0
```

#### Option B: Train Your Own Model

```bash
# Install InstructLab
pip install instructlab

# Initialize InstructLab
ilab config init

# Download base model
ilab model download

# Generate synthetic data from taxonomy
ilab data generate --taxonomy-path ./y

# Train model (requires GPU with 24GB+ VRAM for training)
ilab model train

# Convert to HuggingFace format
ilab model convert

# Copy trained model to project
cp -r ~/.local/share/instructlab/checkpoints/hf_format/samples_0 ./models/
```

#### Option C: Download from HuggingFace

```bash
# Install huggingface-cli
pip install huggingface-hub

# Download a compatible model (example with Mistral-7B)
huggingface-cli download mistralai/Mistral-7B-Instruct-v0.2 --local-dir ./models/samples_0
```

#### Option D: Use Existing Local Models

If you already have a vLLM-compatible model:

```bash
# Copy your model to models/ directory
cp -r /path/to/your/model ./models/samples_0

# Ensure model is in HuggingFace or SafeTensors format
# If you have pytorch_model.bin, convert it:
python convert_to_safetensors.py
```

**Important notes about models:**
- Models are NOT included in the repository due to their large size (5GB-20GB)
- The `models/` directory is excluded in `.gitignore`
- You need to obtain a compatible model before running the project
- vLLM supports models in HuggingFace and SafeTensors formats

### 3. Configure Environment Variables

The `.env` file is already configured with default values:

```bash
# View current configuration
cat .env
```

Important values:
```env
MODEL_PATH=./models/samples_0      # Path to model
VLLM_GPU_MEMORY=0.85               # 85% GPU memory
VLLM_MAX_MODEL_LEN=4096            # Maximum context length
FRONTEND_PORT=80                    # Frontend port
BACKEND_PORT=8000                   # Backend port
```

### 4. Verify GPU (Optional but Recommended)

```bash
# Verify NVIDIA GPU is available
nvidia-smi

# Verify Docker can access GPU
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### 5. Start Services

```bash
# Start all services in detached mode
docker-compose up -d

# View logs in real-time
docker-compose logs -f

# Verify all services are running
docker-compose ps
```

You should see 3 services running:
- `chatbot-frontend` (Nginx)
- `chatbot-backend` (FastAPI)
- `vllm-server` (vLLM with GPU)

### 6. Access the Application

- **Web Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Quick Usage

1. Open your browser at http://localhost
2. Type a message in the text box
3. Press Enter or click "Send"
4. The chatbot will respond using the AI model

**Example questions:**
- "What is machine learning?"
- "Explain what a neural network is"
- "How does natural language processing work?"

## Project Structure

```
instructlab_project/
├── backend/              # FastAPI API
│   ├── app.py           # Main application
│   ├── config.py        # Configuration
│   ├── models.py        # Pydantic models
│   └── services/        # Services (vLLM)
├── frontend/            # Nginx web interface
│   ├── index.html      # Chat UI
│   └── nginx.conf      # Proxy configuration
├── vllm/               # Inference service
│   └── Dockerfile      # vLLM container
├── y/                  # InstructLab Taxonomy
│   ├── knowledge/      # Knowledge by domain
│   ├── compositional_skills/  # Complex skills
│   └── foundational_skills/   # Basic skills
├── models/             # Models (not versioned)
│   └── samples_0/      # Main model
├── docker-compose.yml  # Service orchestration
├── .env               # Environment variables
├── CLAUDE.md          # Complete technical documentation
└── README.md          # This file
```

## Development

### Run Tests

```bash
# Test backend endpoints
python test_backend.py

# Test vLLM chat completions
python test_vllm_chat.py

# Test with improved error handling
python test_vllm_fixed.py
```

### Local Development (Without Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
python -m http.server 3000
# Edit nginx.conf to point to localhost:8000
```

### Add Knowledge to Taxonomy

1. **Navigate to appropriate domain:**
```bash
cd y/knowledge/[domain]/
mkdir my_topic && cd my_topic
```

2. **Create `qna.yaml` file:**
```yaml
created_by: your_name
version: 3
domain: domain_name
task_description: "Description of what this knowledge teaches."
seed_examples:
  - question: "Question 1?"
    answer: "Detailed and accurate answer..."
  - question: "Question 2?"
    answer: "Detailed and accurate answer..."
  # Minimum 5 examples
```

3. **Re-generate data and re-train:**
```bash
ilab data generate --taxonomy-path ./y
ilab model train
```

### Rebuild Services

```bash
# Rebuild specific service
docker-compose up -d --build chatbot-backend

# Rebuild all services
docker-compose up -d --build

# Rebuild without cache
docker-compose build --no-cache
```

## Advanced Configuration

### Adjust Model Parameters

Edit `backend/config.py`:

```python
DEFAULT_MAX_TOKENS = 500        # Increase for longer responses
DEFAULT_TEMPERATURE = 0.7       # 0.0 = deterministic, 1.0 = creative
SYSTEM_PROMPT = "Your prompt..."  # Customize bot behavior
```

### Change Model

```bash
# 1. Place new model in models/
cp -r /path/new_model ./models/new_model

# 2. Update .env
echo "MODEL_PATH=./models/new_model" >> .env

# 3. Restart services
docker-compose down
docker-compose up -d
```

### Optimize for your GPU

Edit `docker-compose.yml`:

```yaml
vllm-server:
  command: >
    --model /models/samples_0
    --gpu-memory-utilization 0.9      # Use more GPU memory
    --max-model-len 8192              # Increase context
    --tensor-parallel-size 2          # Multi-GPU (if you have 2+ GPUs)
```

## Troubleshooting

### vLLM doesn't start / GPU Error

```bash
# Verify GPU available
nvidia-smi

# Check vLLM logs
docker-compose logs vllm-server

# Reduce GPU memory usage in .env
VLLM_GPU_MEMORY=0.7  # Reduce to 70%
```

### Backend can't connect to vLLM

```bash
# Verify vLLM is healthy
curl http://localhost:8080/health

# Check backend logs
docker-compose logs chatbot-backend

# Restart services in order
docker-compose restart vllm-server
docker-compose restart chatbot-backend
```

### Frontend shows "Connection Error"

```bash
# Verify backend is running
curl http://localhost:8000/health

# View Nginx logs
docker-compose logs chatbot-frontend

# Restart frontend
docker-compose restart chatbot-frontend
```

### Model doesn't load / Format Error

```bash
# Convert model to SafeTensors
python convert_to_safetensors.py

# Verify model exists
ls -lh models/samples_0/

# Check read permissions
chmod -R 755 models/samples_0/
```

## Stop Services

```bash
# Stop services (keep containers)
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove everything (containers, volumes, networks)
docker-compose down -v
```

## API Endpoints

### POST /chat
Send message to chatbot.

**Request:**
```json
{
  "message": "What is machine learning?",
  "conversation_history": [],
  "max_tokens": 500,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "response": "Machine learning is...",
  "model": "/models/samples_0",
  "tokens_used": 145,
  "latency_seconds": 2.34
}
```

### GET /health
Check service status.

### GET /models
List available models.

See complete documentation at: http://localhost:8000/docs

## Documentation

- **CLAUDE.md**: Complete technical documentation of the project
- **y/docs/**: Guides for contributing to taxonomy
  - `KNOWLEDGE_GUIDE.md`: How to add knowledge
  - `SKILLS_GUIDE.md`: How to add skills

## External Resources

- [InstructLab Documentation](https://github.com/instructlab/instructlab)
- [vLLM Documentation](https://docs.vllm.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-functionality`)
3. Commit your changes (`git commit -m 'Add new functionality'`)
4. Push to branch (`git push origin feature/new-functionality`)
5. Open a Pull Request

## License

This project is open source and available under the MIT license.

## Author

**Ricardo Honores** - [ricardohonores](https://github.com/ricardohonores)

---

**Note**: This document was developed with assistance from Claude Code to demonstrate integration of InstructLab, vLLM and modern microservices architectures.

## Support

To report bugs or request features, please open an [issue](https://github.com/ricardohonores/instructlab_project/issues).

**[🇪🇸 Ver versión en español](#versión-en-español)**

---
---

<a name="versión-en-español"></a>
# InstructLab Chatbot Educativo

Un chatbot educativo de IA construido con el framework **InstructLab**, optimizado para inferencia de alto rendimiento con **vLLM** y una interfaz web interactiva.

## Características

- **Framework InstructLab**: Fine-tuning de modelos LLM usando taxonomía de conocimientos y habilidades impulsada por la comunidad
- **Inferencia vLLM**: Servidor de inferencia de alto rendimiento con aceleración GPU y API compatible con OpenAI
- **Backend FastAPI**: API REST asíncrona con validación Pydantic y manejo de errores robusto
- **Frontend Web Interactivo**: Interfaz de chat responsive con monitoreo de estado en tiempo real
- **Arquitectura Containerizada**: Despliegue con Docker Compose para fácil orquestación de servicios
- **Health Monitoring**: Checks automáticos de salud y reinicio de servicios
- **Taxonomía Extensible**: Sistema basado en Clasificación Decimal Dewey para organizar conocimientos

## Arquitectura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Frontend   │─────▶│  Backend    │─────▶│    vLLM     │
│   (Nginx)   │      │  (FastAPI)  │      │   (GPU)     │
│   Port: 80  │      │  Port: 8000 │      │ Port: 8000  │
└─────────────┘      └─────────────┘      └─────────────┘
```

**Flujo de datos:**
1. Usuario interactúa con la interfaz web (Nginx)
2. Frontend envía solicitudes al Backend vía `/api/*`
3. Backend procesa solicitud y llama a vLLM para inferencia
4. vLLM ejecuta modelo en GPU y retorna respuesta
5. Backend formatea respuesta con métricas (tokens, latencia)
6. Frontend muestra respuesta al usuario

## Requisitos Previos

- **Docker** y **Docker Compose** (v2.0+)
- **GPU NVIDIA** con drivers CUDA instalados (para vLLM)
- **8GB+ de RAM** (16GB recomendado)
- **Mínimo 10GB de espacio en disco** (sin incluir modelos)
- **Python 3.11+** (para desarrollo local)

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ricardohonores/instructlab_project.git
cd instructlab_project
```

### 2. Obtener el Modelo

Este proyecto requiere un modelo de lenguaje fine-tuned con InstructLab. Tienes varias opciones:

#### Opción A: Usar un Modelo Pre-entrenado de InstructLab

```bash
# Instalar InstructLab CLI
pip install instructlab

# Descargar modelo base de InstructLab
ilab model download

# El modelo se descargará en ~/.local/share/instructlab/models/
# Copiar o crear symlink al directorio del proyecto
mkdir -p models
ln -s ~/.local/share/instructlab/models/merlinite-7b-lab-Q4_K_M.gguf models/samples_0
```

#### Opción B: Entrenar tu Propio Modelo

```bash
# Instalar InstructLab
pip install instructlab

# Inicializar InstructLab
ilab config init

# Descargar modelo base
ilab model download

# Generar datos sintéticos desde la taxonomía
ilab data generate --taxonomy-path ./y

# Entrenar modelo (requiere GPU con 24GB+ VRAM para training)
ilab model train

# Convertir a formato HuggingFace
ilab model convert

# Copiar modelo entrenado al proyecto
cp -r ~/.local/share/instructlab/checkpoints/hf_format/samples_0 ./models/
```

#### Opción C: Descargar desde HuggingFace

```bash
# Instalar huggingface-cli
pip install huggingface-hub

# Descargar un modelo compatible (ejemplo con Mistral-7B)
huggingface-cli download mistralai/Mistral-7B-Instruct-v0.2 --local-dir ./models/samples_0
```

#### Opción D: Usar Modelos Locales Existentes

Si ya tienes un modelo compatible con vLLM:

```bash
# Copiar tu modelo al directorio models/
cp -r /ruta/a/tu/modelo ./models/samples_0

# Asegúrate que el modelo esté en formato HuggingFace o SafeTensors
# Si tienes pytorch_model.bin, conviértelo:
python convert_to_safetensors.py
```

**Nota importante sobre modelos:**
- Los modelos NO están incluidos en el repositorio debido a su gran tamaño (5GB-20GB)
- El directorio `models/` está excluido en `.gitignore`
- Necesitas obtener un modelo compatible antes de ejecutar el proyecto
- vLLM soporta modelos en formato HuggingFace y SafeTensors

### 3. Configurar Variables de Entorno

El archivo `.env` ya está configurado con valores por defecto:

```bash
# Ver configuración actual
cat .env
```

Valores importantes:
```env
MODEL_PATH=./models/samples_0      # Ruta al modelo
VLLM_GPU_MEMORY=0.85               # 85% de memoria GPU
VLLM_MAX_MODEL_LEN=4096            # Longitud máxima de contexto
FRONTEND_PORT=80                    # Puerto del frontend
BACKEND_PORT=8000                   # Puerto del backend
```

### 4. Verificar GPU (Opcional pero Recomendado)

```bash
# Verificar que NVIDIA GPU esté disponible
nvidia-smi

# Verificar que Docker puede acceder a GPU
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### 5. Iniciar los Servicios

```bash
# Iniciar todos los servicios en modo detached
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Verificar que todos los servicios estén corriendo
docker-compose ps
```

Deberías ver 3 servicios corriendo:
- `chatbot-frontend` (Nginx)
- `chatbot-backend` (FastAPI)
- `vllm-server` (vLLM con GPU)

### 6. Acceder a la Aplicación

- **Frontend Web**: http://localhost
- **API Backend**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Uso Rápido

1. Abre tu navegador en http://localhost
2. Escribe un mensaje en el cuadro de texto
3. Presiona Enter o click en "Enviar"
4. El chatbot responderá usando el modelo de IA

**Ejemplos de preguntas:**
- "¿Qué es el aprendizaje automático?"
- "Explícame qué es una red neuronal"
- "¿Cómo funciona el procesamiento de lenguaje natural?"

## Estructura del Proyecto

```
instructlab_project/
├── backend/              # API FastAPI
│   ├── app.py           # Aplicación principal
│   ├── config.py        # Configuración
│   ├── models.py        # Modelos Pydantic
│   └── services/        # Servicios (vLLM)
├── frontend/            # Interfaz web Nginx
│   ├── index.html      # UI de chat
│   └── nginx.conf      # Configuración proxy
├── vllm/               # Servicio de inferencia
│   └── Dockerfile      # Contenedor vLLM
├── y/                  # Taxonomía InstructLab
│   ├── knowledge/      # Conocimientos por dominio
│   ├── compositional_skills/  # Habilidades complejas
│   └── foundational_skills/   # Habilidades básicas
├── models/             # Modelos (no versionados)
│   └── samples_0/      # Modelo principal
├── docker-compose.yml  # Orquestación de servicios
├── .env               # Variables de entorno
├── CLAUDE.md          # Documentación técnica completa
└── README.md          # Este archivo
```

## Desarrollo

### Ejecutar Tests

```bash
# Test de endpoints del backend
python test_backend.py

# Test de chat completions de vLLM
python test_vllm_chat.py

# Test con manejo de errores mejorado
python test_vllm_fixed.py
```

### Desarrollo Local (Sin Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
python -m http.server 3000
# Editar nginx.conf para apuntar a localhost:8000
```

### Agregar Conocimiento a la Taxonomía

1. **Navegar al dominio apropiado:**
```bash
cd y/knowledge/[dominio]/
mkdir mi_tema && cd mi_tema
```

2. **Crear archivo `qna.yaml`:**
```yaml
created_by: tu_nombre
version: 3
domain: nombre_dominio
task_description: "Descripción de qué enseña este conocimiento."
seed_examples:
  - question: "¿Pregunta 1?"
    answer: "Respuesta detallada y precisa..."
  - question: "¿Pregunta 2?"
    answer: "Respuesta detallada y precisa..."
  # Mínimo 5 ejemplos
```

3. **Re-generar datos y re-entrenar:**
```bash
ilab data generate --taxonomy-path ./y
ilab model train
```

### Reconstruir Servicios

```bash
# Reconstruir un servicio específico
docker-compose up -d --build chatbot-backend

# Reconstruir todos los servicios
docker-compose up -d --build

# Reconstruir sin caché
docker-compose build --no-cache
```

## Configuración Avanzada

### Ajustar Parámetros del Modelo

Editar `backend/config.py`:

```python
DEFAULT_MAX_TOKENS = 500        # Aumentar para respuestas más largas
DEFAULT_TEMPERATURE = 0.7       # 0.0 = determinista, 1.0 = creativo
SYSTEM_PROMPT = "Tu prompt..."  # Personalizar comportamiento del bot
```

### Cambiar Modelo

```bash
# 1. Colocar nuevo modelo en models/
cp -r /ruta/nuevo_modelo ./models/nuevo_modelo

# 2. Actualizar .env
echo "MODEL_PATH=./models/nuevo_modelo" >> .env

# 3. Reiniciar servicios
docker-compose down
docker-compose up -d
```

### Optimizar para tu GPU

Editar `docker-compose.yml`:

```yaml
vllm-server:
  command: >
    --model /models/samples_0
    --gpu-memory-utilization 0.9      # Usar más memoria GPU
    --max-model-len 8192              # Aumentar contexto
    --tensor-parallel-size 2          # Multi-GPU (si tienes 2+ GPUs)
```

## Troubleshooting

### vLLM no inicia / Error de GPU

```bash
# Verificar GPU disponible
nvidia-smi

# Verificar logs de vLLM
docker-compose logs vllm-server

# Reducir uso de memoria GPU en .env
VLLM_GPU_MEMORY=0.7  # Reducir a 70%
```

### Backend no conecta a vLLM

```bash
# Verificar que vLLM esté healthy
curl http://localhost:8080/health

# Verificar logs del backend
docker-compose logs chatbot-backend

# Reiniciar servicios en orden
docker-compose restart vllm-server
docker-compose restart chatbot-backend
```

### Frontend muestra "Error de conexión"

```bash
# Verificar que backend esté corriendo
curl http://localhost:8000/health

# Ver logs de Nginx
docker-compose logs chatbot-frontend

# Reiniciar frontend
docker-compose restart chatbot-frontend
```

### Modelo no carga / Error de formato

```bash
# Convertir modelo a SafeTensors
python convert_to_safetensors.py

# Verificar que el modelo existe
ls -lh models/samples_0/

# Verificar permisos de lectura
chmod -R 755 models/samples_0/
```

## Detener Servicios

```bash
# Detener servicios (mantener contenedores)
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Eliminar todo (contenedores, volúmenes, redes)
docker-compose down -v
```

## API Endpoints

### POST /chat
Envía mensaje al chatbot.

**Request:**
```json
{
  "message": "¿Qué es el machine learning?",
  "conversation_history": [],
  "max_tokens": 500,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "response": "El machine learning es...",
  "model": "/models/samples_0",
  "tokens_used": 145,
  "latency_seconds": 2.34
}
```

### GET /health
Verifica estado de servicios.

### GET /models
Lista modelos disponibles.

Ver documentación completa en: http://localhost:8000/docs

## Documentación

- **CLAUDE.md**: Documentación técnica completa del proyecto
- **y/docs/**: Guías para contribuir a la taxonomía
  - `KNOWLEDGE_GUIDE.md`: Cómo agregar conocimiento
  - `SKILLS_GUIDE.md`: Cómo agregar habilidades

## Recursos Externos

- [InstructLab Documentation](https://github.com/instructlab/instructlab)
- [vLLM Documentation](https://docs.vllm.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

**Ricardo Honores** - [ricardohonores](https://github.com/ricardohonores)

---

**Nota**: Este documento fue desarrollado con asistencia de Claude Code para demostrar integración de InstructLab, vLLM y arquitecturas modernas de microservicios.

## Soporte

Para reportar bugs o solicitar features, por favor abre un [issue](https://github.com/ricardohonores/instructlab_project/issues).

**[🇬🇧 View English version](#english-version)**
