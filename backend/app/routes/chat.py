from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ChatRequest, ChatResponse
from ..rag import obter_resposta_rag

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
# utilizacao de schemas para validar os dados de entrada e saida
# injecao de dependencias para obter a sessao do banco de dados
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        resultado = obter_resposta_rag(request.question, db)
        
        return ChatResponse(
            answer=resultado["answer"],
            sources=resultado["sources"]
        )
    except ValueError as e:
        # Erros conhecidos (rate limit, API key, etc)
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        # Outros erros inesperados
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

