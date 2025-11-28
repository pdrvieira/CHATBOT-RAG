# Chat RAG para Petshop 🐾

Chat inteligente que responde perguntas sobre um petshop usando RAG (Retrieval Augmented Generation). O sistema busca informações relevantes no banco de dados e gera respostas contextualizadas com LLM.

## 🛠️ Tecnologias

### Backend
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM para SQLite
- **SQLite** - Banco de dados
- **Sentence Transformers** - Modelo BGE-small para embeddings
- **LangChain** - Integração com LLMs
- **Qwen 2.5** - LLM via OpenRouter
- **Pytest** - Testes

### Frontend
- **React** - Biblioteca UI
- **TypeScript** - Tipagem estática
- **Vite** - Build tool
- **Tailwind CSS** - Estilização

## 🧠 Como Funciona o RAG

1. **Usuário faz uma pergunta** no chat
2. **Backend gera embedding da pergunta** usando BGE-small
3. **Busca documentos similares** no banco (cálculo de similaridade cosseno)
4. **Seleciona os top-3 documentos** mais relevantes
5. **Monta um contexto** juntando os documentos
6. **Envia para o LLM** (Qwen 2.5) com o contexto
7. **Retorna a resposta** para o frontend com as fontes usadas

```
Pergunta → Embedding → Busca Vetorial → Contexto → LLM → Resposta
```

## 📁 Estrutura do Projeto

```
chatbot-RAG/
├── backend/
│   ├── app/
│   │   ├── main.py           # entrada da aplicação
│   │   ├── database.py       # configuração SQLite
│   │   ├── models.py         # modelo Document
│   │   ├── schemas.py        # schemas Pydantic
│   │   ├── embeddings.py     # BGE-small + similaridade
│   │   ├── llm.py            # integração LangChain + Qwen
│   │   ├── rag.py            # pipeline RAG completo
│   │   └── routes/
│   │       └── chat.py       # endpoint /chat
│   ├── tests/
│   │   ├── test_rag.py       # testes de retrieval
│   │   └── test_chat.py      # testes de montagem de contexto
│   ├── seed.py               # popula o banco com docs do petshop
│   ├── testar_modelos.py     # script para testar modelos
│   ├── requirements.txt
│   └── .env                  # variáveis de ambiente (criar manualmente)
│
└── frontend/
    ├── src/
    │   ├── components/       # componentes reutilizáveis
    │   ├── sections/         # seções da página
    │   ├── services/         # chamadas API
    │   ├── lib/              # tipos TypeScript
    │   ├── assets/           # imagens e recursos
    │   └── styles/           # estilos CSS
    ├── package.json
    └── vite.config.ts
```

## 🚀 Como Rodar

### Backend

1. **Clone o repositório**
```bash
git clone <seu-repo>
cd chatbot-RAG/backend
```

2. **Crie um ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente IMPORTANTE**
```bash
# Crie um arquivo .env na pasta backend/ com o seguinte conteúdo:
# OPENROUTER_API_KEY=sua_chave_aqui
# 
# Obtenha sua chave em: https://openrouter.ai/keys
```

5. **Popule o banco de dados**
```bash
python seed.py
```

6. **Rode o servidor**
```bash
uvicorn app.main:app --reload
```

O backend estará rodando em `http://localhost:8000`

### Frontend

1. **Entre na pasta do frontend**
```bash
cd ../frontend
```

2. **Instale as dependências**
```bash
npm install
```

3. **Rode o servidor de desenvolvimento**
```bash
npm run dev
```

O frontend estará rodando em `http://localhost:5173`

## 🧪 Testes

```bash
cd backend
pytest tests/ -v
```

**Cobertura:**
- Retrieval de documentos por similaridade
- Parâmetro top_k
- Montagem de contexto
- Estrutura de resposta do RAG

## 📝 Endpoints

### `POST /chat`

Envia uma pergunta e recebe uma resposta contextualizada.

**Request:**
```json
{
  "question": "Qual o horário de funcionamento?"
}
```

**Response:**
```json
{
  "answer": "O petshop funciona de segunda a sexta das 9h às 19h...",
  "sources": ["Horário de Funcionamento", "Serviços"]
}
```

### `GET /health`

Verifica se o servidor está rodando.

**Response:**
```json
{
  "status": "ok"
}
```

## 🎯 Características

- ✅ RAG funcional com busca vetorial
- ✅ Embeddings locais (BGE-small)
- ✅ LLM integrado via LangChain
- ✅ Frontend React moderno e responsivo
- ✅ Testes com fixtures e mocks
- ✅ Código limpo e bem estruturado
- ✅ API RESTful documentada

## 📦 Dependências Principais

**Backend:**
- `fastapi==0.109.0`
- `sqlalchemy==2.0.36`
- `sentence-transformers==2.3.1`
- `langchain==0.3.17`
- `pytest==7.4.4`

**Frontend:**
- `react==18.3.1`
- `typescript==5.5.3`
- `vite==5.4.2`
- `tailwindcss==3.4.10`

## 🔧 Próximas Melhorias Possiveis...

- [ ] Adicionar histórico de conversação
- [ ] Implementar auto-scroll no chat
- [ ] Cache de embeddings
- [ ] Deploy em produção
- [ ] Mais testes de integração

## 📄 Licença

MIT

---

Feito com ❤️ para demonstração de RAG com FastAPI + React
