import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def configurar_llm():
    # para testar esse codigo apos clona-lo é necessário criar um arquivo .env
    # com a variável OPENROUTER_API_KEY contendo a chave da OpenRouter que voces criou
    # no site https://openrouter.ai/ usando API do deepseek/deepseek-r1-0528-qwen3-8b:free
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY não encontrada no .env")
    
    return ChatOpenAI(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_tokens=500
    )


def gerar_resposta(pergunta: str, contexto: str) -> str:
    llm = configurar_llm()
    
    # monta o prompt com as instruções
    prompt = f"""Você é um assistente virtual de um petshop. Use apenas as informações do contexto abaixo para responder.
Se a informação não estiver no contexto, diga que não tem essa informação disponível.

Contexto:
{contexto}

Pergunta: {pergunta}

Resposta:"""
    
    # chama o modelo
    resposta = llm.invoke(prompt)
    
    return resposta.content.strip()

