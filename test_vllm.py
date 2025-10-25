import requests
import json
import time

API_URL = "http://localhost:8080/v1/completions"

def wait_for_server():
    print("⏳ Esperando que el servidor esté listo...")
    for i in range(60):
        try:
            response = requests.get("http://localhost:8080/health", timeout=2)
            if response.status_code == 200:
                print("✅ Servidor listo!")
                return True
        except:
            time.sleep(5)
            print(f"   Intento {i+1}/60...")
    return False

def chat(prompt):
    payload = {
        "model": "instructlab/granite-7b-lab",
        "prompt": f"Usuario: {prompt}\nAsistente:",
        "max_tokens": 300,
        "temperature": 0.7,
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    return result['choices'][0]['text'].strip()

if __name__ == "__main__":
    if not wait_for_server():
        print("❌ Servidor no respondió")
        exit(1)
    
    print("\n" + "="*60)
    print("🤖 Probando el modelo fine-tuneado")
    print("="*60)
    
    questions = [
        "¿Qué es la personalización del aprendizaje con IA?",
        "¿Cómo ayuda la IA a los profesores?",
    ]
    
    for q in questions:
        print(f"\n👤 P: {q}")
        answer = chat(q)
        print(f"🤖 R: {answer}")
        print("-"*60)

