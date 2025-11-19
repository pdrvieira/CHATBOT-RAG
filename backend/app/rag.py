import json
from sqlalchemy.orm import Session
from .models import Document
from .embeddings import gerar_embedding, calcular_similaridade
from .llm import gerar_resposta


def retrieve_docs(pergunta: str, db: Session, top_k: int = 3):
    # gera embedding da pergunta
    embedding_pergunta = gerar_embedding(pergunta)
    
    # pega todos os docs do banco
    todos_docs = db.query(Document).all()
    
    # calcula similaridade com cada doc
    resultados = []
    for doc in todos_docs:
        embedding_doc = json.loads(doc.embedding)
        score = calcular_similaridade(embedding_pergunta, embedding_doc)
        resultados.append((doc, score))
    
    # ordena por score (maior = mais similar) e pega os top_k
    resultados.sort(key=lambda x: x[1], reverse=True)
    docs_relevantes = [doc for doc, _ in resultados[:top_k]]
    
    return docs_relevantes


def montar_contexto(documentos):
    # junta os documentos num contexto único
    partes = []
    for doc in documentos:
        partes.append(f"# {doc.titulo}\n{doc.conteudo}")
    
    return "\n\n".join(partes)


def obter_resposta_rag(pergunta: str, db: Session):
    # busca docs mais relevantes
    docs_relevantes = retrieve_docs(pergunta, db, top_k=3)
    
    # monta o contexto com esses docs
    contexto = montar_contexto(docs_relevantes)
    
    # gera resposta usando LLM
    resposta = gerar_resposta(pergunta, contexto)
    
    # retorna resposta + fontes usadas
    return {
        "answer": resposta,
        "sources": [doc.titulo for doc in docs_relevantes]
    }

