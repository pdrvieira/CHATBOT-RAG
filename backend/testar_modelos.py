#!/usr/bin/env python3
#Script para testar vários modelos gratuitos e encontrar qual está disponível


import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Lista de modelos gratuitos para testar (nomes corretos do OpenRouter)
MODELOS_PARA_TESTAR = [
    "google/gemini-flash-1.5",
    "qwen/qwen-2.5-7b-instruct",
    "mistralai/mistral-7b-instruct",
    "meta-llama/llama-3.2-3b-instruct",
    "deepseek/deepseek-r1-0528-qwen3-8b",
    "microsoft/phi-3-mini-4k-instruct",
    "huggingface/meta-llama/Meta-Llama-3.1-8B-Instruct",
    "google/gemini-pro-1.5",
]

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("❌ OPENROUTER_API_KEY não encontrada no .env")
    exit(1)

print("🔍 Testando modelos gratuitos disponíveis...\n")
print("=" * 60)

modelos_funcionando = []
modelos_com_erro = []

for modelo in MODELOS_PARA_TESTAR:
    print(f"\n🧪 Testando: {modelo}")
    print("-" * 60)
    
    try:
        # Configura LLM
        llm = ChatOpenAI(
            model=modelo,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.7,
            max_tokens=50  # Resposta curta para teste rápido
        )
        
        # Faz chamada de teste
        resposta = llm.invoke("Responda apenas: OK")
        resposta_texto = resposta.content.strip()
        
        print(f"✅ FUNCIONOU! Resposta: {resposta_texto[:50]}...")
        modelos_funcionando.append(modelo)
        
    except Exception as e:
        error_str = str(e).lower()
        
        if "429" in error_str or "rate limit" in error_str or "rate-limited" in error_str:
            print(f"⚠️  Rate limit (sobrecarregado temporariamente)")
            modelos_com_erro.append((modelo, "rate_limit"))
        elif "401" in error_str or "unauthorized" in error_str:
            print(f"❌ Erro de autenticação")
            modelos_com_erro.append((modelo, "auth"))
        elif "404" in error_str or "not found" in error_str:
            print(f"❌ Modelo não encontrado")
            modelos_com_erro.append((modelo, "not_found"))
        else:
            print(f"❌ Erro: {str(e)[:100]}")
            modelos_com_erro.append((modelo, "other"))

print("\n" + "=" * 60)
print("\n📊 RESULTADO FINAL:\n")

if modelos_funcionando:
    print("✅ MODELOS FUNCIONANDO:")
    for i, modelo in enumerate(modelos_funcionando, 1):
        print(f"   {i}. {modelo}")
    print("\n💡 Você pode usar qualquer um desses no llm.py!")
else:
    print("⚠️  Nenhum modelo funcionou no momento.")
    print("   Todos estão com rate limit ou erro temporário.")
    print("   Tente novamente em alguns minutos.")

if modelos_com_erro:
    print(f"\n❌ Modelos com problemas: {len(modelos_com_erro)}")

print("\n" + "=" * 60)

