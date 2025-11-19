import pytest
from unittest.mock import patch, Mock
from app.rag import obter_resposta_rag, montar_contexto
from app.models import Document


def test_montar_contexto():
    # cria docs fake pra testar a montagem do contexto
    primeiro_doc = Mock(spec=Document)
    primeiro_doc.titulo = "Horário"
    primeiro_doc.conteudo = "Das 9h às 19h"
    
    segundo_doc = Mock(spec=Document)
    segundo_doc.titulo = "Endereço"
    segundo_doc.conteudo = "Rua X, 123"
    
    contexto_montado = montar_contexto([primeiro_doc, segundo_doc])
    
    # tem que ter os dois docs no contexto
    assert "Horário" in contexto_montado
    assert "Das 9h às 19h" in contexto_montado
    assert "Endereço" in contexto_montado
    assert "Rua X, 123" in contexto_montado


def test_obter_resposta_rag_retorna_estrutura_correta():
    # mocka tudo pra não bater no banco nem na API
    with patch("app.rag.retrieve_docs") as mock_busca:
        with patch("app.rag.gerar_resposta") as mock_llm:
            doc_fake = Mock(spec=Document)
            doc_fake.titulo = "Teste"
            doc_fake.conteudo = "Conteúdo teste"
            
            mock_busca.return_value = [doc_fake]
            mock_llm.return_value = "Resposta do LLM"
            
            resposta = obter_resposta_rag("pergunta teste", Mock())
            
            # verifica se tem a estrutura certa
            assert "answer" in resposta
            assert "sources" in resposta
            assert resposta["answer"] == "Resposta do LLM"
            assert resposta["sources"] == ["Teste"]
            
            # garante que chamou o LLM
            assert mock_llm.called
