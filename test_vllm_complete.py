import requests
import json
import time

API_URL = "http://localhost:8080"

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

def chat(prompt, max_tokens=300):
    """Enviar un mensaje al modelo"""
    payload = {
        "model": "samples_0",
        "prompt": f"Usuario: {prompt}\nAsistente:",
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "stop": ["Usuario:", "\n\n"]
    }
    
    print(f"📤 Enviando: {prompt}")
    start_time = time.time()
    
    response = requests.post(f"{API_URL}/v1/completions", json=payload)
    
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        answer = result['choices'][0]['text'].strip()
        tokens = result['usage']['total_tokens']
        
        print(f"✅ Respuesta ({elapsed:.2f}s, {tokens} tokens):")
        print(f"🤖 {answer}\n")
        return answer
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None

def main():
    print("="*70)
    print("🚀 Probando vLLM Server con tu modelo fine-tuneado")
    print("="*70)
    
    # 1. Verificar health
    print("\n1️⃣ Verificando servidor...")
    if check_health():
        print("✅ Servidor activo")
    else:
        print("❌ Servidor no responde")
        return
    
    # 2. Listar modelos
    print("\n2️⃣ Modelos disponibles:")
    models = get_models()
    for model in models['data']:
        print(f"   📦 {model['id']}")
    
    # 3. Probar con preguntas de tu dominio
    print("\n3️⃣ Probando conocimiento fine-tuneado:")
    print("-"*70)
    
    questions = [
        "¿Qué es la personalización del aprendizaje con IA?",
        "¿Cómo puede la IA ayudar a los profesores?",
        "Explícame qué es la tutoría inteligente",
        "¿Qué beneficios tiene la automatización de tareas educativas?"
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\n📝 Pregunta {i}/{len(questions)}")
        print("-"*70)
        chat(q)
        time.sleep(1)  # Pausa entre preguntas
    
    print("\n" + "="*70)
    print("✅ Prueba completada!")
    print("="*70)

if __name__ == "__main__":
    main()
