# Usar imagen más reciente y compatible
FROM vllm/vllm-openai:latest

# Instalar curl para health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Configurar variables de entorno
ENV CUDA_VISIBLE_DEVICES=0

# Exponer puerto
EXPOSE 8000
