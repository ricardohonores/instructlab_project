import requests
import json
import time

API_URL = "http://localhost:8000"

def print_separator():
    print("\n" + "="*70 + "\n")

def test_health():
    """Test health endpoint"""
    print("1️⃣  Testing /health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("2️⃣  Testing / endpoint...")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_models():
    """Test models endpoint"""
    print("3️⃣  Testing /models endpoint...")
    try:
        response = requests.get(f"{API_URL}/models", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Models available: {len(data.get('data', []))}")
            return True
        else:
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_simple_chat():
    """Test simple chat without history"""
    print("4️⃣  Testing /chat endpoint (simple)...")
    
    payload = {
        "message": "¿Qué es la personalización del aprendizaje con IA?",
        "max_tokens": 200,
        "temperature": 0.7
    }
    
    print(f"   📤 Pregunta: {payload['message']}")
    
    try:
        start = time.time()
        response = requests.post(f"{API_URL}/chat", json=payload, timeout=120)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Respuesta recibida en {elapsed:.2f}s")
            print(f"   📊 Tokens: {result['tokens_used']} total")
            print(f"       - Prompt: {result['prompt_tokens']}")
            print(f"       - Completion: {result['completion_tokens']}")
            print(f"   🤖 Respuesta (primeros 150 chars):")
            print(f"       {result['response'][:150]}...")
            return True
        else:
            print(f"   ❌ Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️  Timeout después de 120s")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_chat_with_history():
    """Test chat with conversation history"""
    print("5️⃣  Testing /chat endpoint (with history)...")
    
    # Primera pregunta
    payload1 = {
        "message": "¿Qué es la IA en educación?",
        "max_tokens": 150
    }
    
    print(f"   📤 Pregunta 1: {payload1['message']}")
    
    try:
        response1 = requests.post(f"{API_URL}/chat", json=payload1, timeout=120)
        
        if response1.status_code != 200:
            print(f"   ❌ Primera pregunta falló: {response1.status_code}")
            return False
        
        result1 = response1.json()
        answer1 = result1['response']
        print(f"   🤖 Respuesta 1 (primeros 100 chars): {answer1[:100]}...")
        
        # Segunda pregunta con contexto
        payload2 = {
            "message": "¿Puedes darme un ejemplo concreto?",
            "conversation_history": [
                {"role": "user", "content": payload1["message"]},
                {"role": "assistant", "content": answer1}
            ],
            "max_tokens": 150
        }
        
        print(f"   📤 Pregunta 2 (con contexto): {payload2['message']}")
        
        response2 = requests.post(f"{API_URL}/chat", json=payload2, timeout=120)
        
        if response2.status_code == 200:
            result2 = response2.json()
            answer2 = result2['response']
            print(f"   🤖 Respuesta 2 (primeros 100 chars): {answer2[:100]}...")
            print(f"   ✅ Conversación con contexto funcionando")
            return True
        else:
            print(f"   ❌ Segunda pregunta falló: {response2.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_edge_cases():
    """Test edge cases and validation"""
    print("6️⃣  Testing edge cases...")
    
    # Test 1: Mensaje vacío
    print("   - Probando mensaje vacío...")
    response = requests.post(f"{API_URL}/chat", json={"message": ""})
    if response.status_code == 422:
        print("     ✅ Validación de mensaje vacío OK")
    else:
        print(f"     ⚠️  Esperaba 422, obtuvo {response.status_code}")
    
    # Test 2: Max tokens fuera de rango
    print("   - Probando max_tokens fuera de rango...")
    response = requests.post(f"{API_URL}/chat", json={
        "message": "Test",
        "max_tokens": 5000  # Límite es 2000
    })
    if response.status_code == 422:
        print("     ✅ Validación de max_tokens OK")
    else:
        print(f"     ⚠️  Esperaba 422, obtuvo {response.status_code}")
    
    # Test 3: Temperature fuera de rango
    print("   - Probando temperature fuera de rango...")
    response = requests.post(f"{API_URL}/chat", json={
        "message": "Test",
        "temperature": 3.0  # Límite es 2.0
    })
    if response.status_code == 422:
        print("     ✅ Validación de temperature OK")
    else:
        print(f"     ⚠️  Esperaba 422, obtuvo {response.status_code}")
    
    return True

def main():
    print_separator()
    print("🧪 SUITE DE PRUEBAS - BACKEND FASTAPI")
    print_separator()
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Models Endpoint", test_models),
        ("Simple Chat", test_simple_chat),
        ("Chat with History", test_chat_with_history),
        ("Edge Cases", test_edge_cases),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Error ejecutando test: {e}")
            results.append((name, False))
        
        print_separator()
        time.sleep(1)
    
    # Resumen
    print("📊 RESUMEN DE PRUEBAS")
    print_separator()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print_separator()
    print(f"Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡Todos los tests pasaron!")
    else:
        print("⚠️  Algunas pruebas fallaron")
    
    print_separator()

if __name__ == "__main__":
    main()
