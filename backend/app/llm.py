import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def configurar_llm():
    # para testar esse codigo apos clona-lo é necessário criar um arquivo .env
    # com a variável OPENROUTER_API_KEY contendo a chave da OpenRouter que voces criou
    # no site https://openrouter.ai/ usando qualquer modelo disponível
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY não encontrada no .env")
    
    return ChatOpenAI(
        model="qwen/qwen-2.5-7b-instruct",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_tokens=500
    )


def gerar_resposta(pergunta: str, contexto: str) -> str:
    try:
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
    except Exception as e:
        error_str = str(e).lower()
        
        # Trata erro de rate limit (429)
        if "429" in error_str or "rate limit" in error_str or "rate-limited" in error_str:
            raise ValueError(
                "O modelo de IA está temporariamente sobrecarregado (limite de requisições). "
                "Por favor, aguarde alguns minutos e tente novamente. "
                "Ou adicione sua própria API key em https://openrouter.ai/settings/integrations"
            )
        
        # Trata erro de API key inválida
        if "401" in error_str or "unauthorized" in error_str:
            raise ValueError("API key inválida. Verifique sua chave no arquivo .env")
        
        # Outros erros
        raise ValueError(f"Erro ao gerar resposta: {str(e)}")

