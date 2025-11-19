import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Document
from app.embeddings import gerar_embedding
from app.rag import retrieve_docs
import json


@pytest.fixture
def db_session():
    # banco em memória pro teste não bagunçar o real
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    sessao = Session()
    
    # alguns docs fake pra testar
    documentos_fake = [
        {
            "titulo": "Horário de Funcionamento",
            "conteudo": "Abrimos de segunda a sexta das 9h às 19h."
        },
        {
            "titulo": "Serviços de Banho",
            "conteudo": "Oferecemos banho e tosa para cães e gatos."
        },
        {
            "titulo": "Ração Premium",
            "conteudo": "Vendemos rações das melhores marcas do mercado."
        }
    ]
    
    for item in documentos_fake:
        texto_completo = f"{item['titulo']} {item['conteudo']}"
        vetor = gerar_embedding(texto_completo)
        
        documento = Document(
            titulo=item["titulo"],
            conteudo=item["conteudo"],
            embedding=json.dumps(vetor)
        )
        sessao.add(documento)
    
    sessao.commit()
    yield sessao
    sessao.close()


def test_retrieve_docs_retorna_documentos_relevantes(db_session):
    pergunta = "Qual o horário de funcionamento?"
    
    resultados = retrieve_docs(pergunta, db_session, top_k=2)
    
    assert len(resultados) == 2
    # o doc mais relevante tem que ser sobre horário
    assert "Horário" in resultados[0].titulo


def test_retrieve_docs_com_top_k_diferente(db_session):
    pergunta = "serviços"
    resultados = retrieve_docs(pergunta, db_session, top_k=1)
    
    # pediu 1, tem que vir 1
    assert len(resultados) == 1


def test_retrieve_docs_retorna_objetos_document(db_session):
    # verifica se volta Document de verdade, não dict ou string
    pergunta = "ração"
    resultados = retrieve_docs(pergunta, db_session, top_k=3)
    
    for item in resultados:
        assert isinstance(item, Document)
        assert hasattr(item, "titulo")
        assert hasattr(item, "conteudo")
        assert hasattr(item, "embedding")

