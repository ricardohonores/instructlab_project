"""
Servidor vLLM con modelo fine-tuneado de InstructLab
Versión corregida para vLLM 0.11.0
"""

import asyncio
import argparse
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.entrypoints.openai.api_server import run_server
from vllm.entrypoints.openai.cli_args import make_arg_parser
import os

def create_parser():
    """Crear parser con los argumentos necesarios"""
    parser = make_arg_parser()
    
    # Argumentos personalizados adicionales si los necesitas
    parser.add_argument('--lora-adapter', type=str,
                       default='/home/honores/.local/share/instructlab/checkpoints/hf_format/samples_0',
                       help='Ruta al adaptador LoRA')
    
    return parser

async def main():
    # Crear el parser usando la función de vLLM
    parser = create_parser()
    args = parser.parse_args()
    
    # Configurar el adaptador LoRA si se proporcionó
    if args.lora_adapter and os.path.exists(args.lora_adapter):
        args.enable_lora = True
        args.max_lora_rank = 8
        args.lora_modules = [{
            "name": "education-lora",
            "path": args.lora_adapter
        }]
        print(f"🎯 LoRA adapter configurado: {args.lora_adapter}")
    
    print(f"🚀 Iniciando vLLM Server...")
    print(f"📦 Modelo: {args.model}")
    print(f"🌐 Servidor: {args.host}:{args.port}")
    print(f"💾 GPU Memory: {args.gpu_memory_utilization}")
    
    # Ejecutar el servidor
    await run_server(args)

if __name__ == "__main__":
    asyncio.run(main())
