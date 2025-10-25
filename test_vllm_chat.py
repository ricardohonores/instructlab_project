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
    """Enviar un mensaje usando chat completions"""
    
    # Intentar primero con /v1/chat/completions
    payload_chat = {
        "model": "samples_0",
        "messages": [
            {"role": "system", "content": "Eres un asistente experto en IA aplicada a la educación."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    print(f"📤 Enviando: {prompt}")
    start_time = time.time()
    
    # Intentar endpoint de chat
    response = requests.post(f"{API_URL}/v1/chat/completions", json=payload_chat)
    
    if response.status_code == 200:
        elapsed = time.time() - start_time
        result = response.json()
        answer = result['choices'][0]['message']['content'].strip()
        tokens = result['usage']['total_tokens']
        
        print(f"✅ Respuesta ({elapsed:.2f}s, {tokens} tokens):")
        print(f"🤖 {answer}\n")
        return answer
    
    # Si falla, intentar con generate (algunas versiones usan esto)
    elif response.status_code == 404:
        print("⚠️  /v1/chat/completions no disponible, intentando /generate...")
        
        payload_generate = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        response = requests.post(f"{API_URL}/generate", json=payload_generate)
        
        if response.status_code == 200:
            elapsed = time.time() - start_time
            result = response.json()
            answer = result.get('text', [None])[0] if isinstance(result.get('text'), list) else result.get('text', '')
            
            print(f"✅ Respuesta ({elapsed:.2f}s):")
            print(f"🤖 {answer}\n")
            return answer
    
    print(f"❌ Error {response.status_code}: {response.text}")
    return None

def list_endpoints():
    """Intentar descubrir qué endpoints están disponibles"""
    print("\n🔍 Descubriendo endpoints disponibles...")
    
    endpoints_to_try = [
        "/v1/completions",
        "/v1/chat/completions", 
        "/generate",
        "/v1/generate",
        "/v1/engines",
        "/tokenize"
    ]
    
    available = []
    for endpoint in endpoints_to_try:
        try:
            # GET request
            response = requests.get(f"{API_URL}{endpoint}", timeout=2)
            if response.status_code != 404:
                available.append(f"{endpoint} (GET: {response.status_code})")
        except:
            pass
        
        try:
            # POST request con payload vacío
            response = requests.post(f"{API_URL}{endpoint}", json={}, timeout=2)
            if response.status_code != 404:
                available.append(f"{endpoint} (POST: {response.status_code})")
        except:
            pass
    
    if available:
        print("✅ Endpoints encontrados:")
        for ep in available:
            print(f"   - {ep}")
    else:
        print("❌ No se encontraron endpoints conocidos")
    
    return available

def main():
    print("="*70)
    print("🚀 Probando vLLM Server - Diagnóstico completo")
    print("="*70)
    
    # 1. Verificar health
    print("\n1️⃣ Verificando servidor...")
    if check_health():
        print("✅ Servidor activo en", API_URL)
    else:
        print("❌ Servidor no responde")
        return
    
    # 2. Listar modelos
    print("\n2️⃣ Modelos disponibles:")
    try:
        models = get_models()
        for model in models['data']:
            print(f"   📦 {model['id']}")
            model_id = model['id']  # Guardar para usar después
    except Exception as e:
        print(f"❌ Error obteniendo modelos: {e}")
        return
    
    # 3. Descubrir endpoints
    list_endpoints()
    
    # 4. Probar con preguntas
    print("\n3️⃣ Probando modelo:")
    print("-"*70)
    
    questions = [
        "¿Qué es la personalización del aprendizaje con IA?",
        "¿Cómo puede la IA ayudar a los profesores?"
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\n📝 Pregunta {i}/{len(questions)}")
        print("-"*70)
        chat(q)
        time.sleep(1)
    
    print("\n" + "="*70)
    print("✅ Diagnóstico completado!")
    print("="*70)

if __name__ == "__main__":
    main()
