import requests
import json
import time

API_URL = "http://localhost:8080"

# Nombre completo del modelo según vLLM
MODEL_NAME = "/home/honores/.local/share/instructlab/checkpoints/hf_format/samples_0"

def check_health():
    """Verificar que el servidor está activo"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_models():
    """Obtener lista de modelos disponibles"""
    response = requests.get(f"{API_URL}/v1/models")
    return response.json()

def chat_completion(prompt, max_tokens=300):
    """Enviar mensaje usando chat completions API"""
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system", 
                "content": "Eres un asistente experto en IA aplicada a la educación."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "stream": False
    }
    
    print(f"📤 Pregunta: {prompt}")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/v1/chat/completions", 
            json=payload,
            timeout=120  # Timeout generoso
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content'].strip()
            
            # Obtener estadísticas si están disponibles
            usage = result.get('usage', {})
            prompt_tokens = usage.get('prompt_tokens', '?')
            completion_tokens = usage.get('completion_tokens', '?')
            total_tokens = usage.get('total_tokens', '?')
            
            print(f"✅ Respuesta en {elapsed:.2f}s")
            print(f"📊 Tokens: {prompt_tokens} prompt + {completion_tokens} completion = {total_tokens} total")
            print(f"🤖 {answer}")
            print()
            return answer
        else:
            print(f"❌ Error {response.status_code}")
            print(f"Detalles: {response.text}")
            print()
            return None
            
    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout después de 120s")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def text_completion(prompt, max_tokens=300):
    """Enviar mensaje usando completions API (alternativa)"""
    
    payload = {
        "model": MODEL_NAME,
        "prompt": f"Usuario: {prompt}\nAsistente:",
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "stop": ["Usuario:", "\n\n"],
        "stream": False
    }
    
    print(f"📤 Pregunta: {prompt}")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/v1/completions", 
            json=payload,
            timeout=120
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['text'].strip()
            
            usage = result.get('usage', {})
            total_tokens = usage.get('total_tokens', '?')
            
            print(f"✅ Respuesta en {elapsed:.2f}s ({total_tokens} tokens)")
            print(f"🤖 {answer}")
            print()
            return answer
        else:
            print(f"❌ Error {response.status_code}")
            print(f"Detalles: {response.text}")
            print()
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("="*80)
    print("🚀 Prueba Completa de vLLM Server")
    print("="*80)
    
    # 1. Health check
    print("\n1️⃣ Verificando servidor...")
    if not check_health():
        print("❌ Servidor no disponible")
        return
    print("✅ Servidor activo\n")
    
    # 2. Listar modelos
    print("2️⃣ Modelo cargado:")
    try:
        models = get_models()
        print(f"   📦 {models['data'][0]['id']}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return
    
    # 3. Probar chat completions
    print("3️⃣ Probando con Chat Completions API:")
    print("-"*80)
    
    questions = [
        "¿Qué es la personalización del aprendizaje con IA?",
        "¿Cómo ayuda la IA a automatizar tareas educativas?",
        "Explícame qué es la tutoría inteligente",
    ]
    
    success_count = 0
    
    for i, q in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}]")
        result = chat_completion(q)
        if result:
            success_count += 1
        time.sleep(1)
    
    # 4. Si chat completions falló, probar text completions
    if success_count == 0:
        print("\n⚠️  Chat completions no funcionó, probando Text Completions API:")
        print("-"*80)
        
        for i, q in enumerate(questions[:2], 1):
            print(f"\n[{i}/2]")
            result = text_completion(q)
            if result:
                success_count += 1
            time.sleep(1)
    
    # Resumen
    print("\n" + "="*80)
    if success_count > 0:
        print(f"✅ Prueba exitosa! {success_count} respuestas generadas correctamente")
    else:
        print("❌ No se pudo obtener respuestas del modelo")
    print("="*80)

if __name__ == "__main__":
    main()
