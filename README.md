# 🤖 Capitão IA

Sistema de agente de IA com memória conversacional, construído com FastAPI, PostgreSQL e Google Gemini.

## 📋 Visão Geral

O Capitão IA é um assistente inteligente que pode:
- Manter conversas contextualizadas com memória persistente
- Integrar com ferramentas externas (Notion)
- Processar perguntas e fornecer respostas personalizadas
- Gerar resumos de tickets por cliente

## 🏗️ Arquitetura

```
app/
├── agents/           # Lógica dos agentes IA
│   ├── main_agent.py # Agente principal de chat
│   ├── models/       # Modelos de IA (Gemini)
│   └── tools/        # Ferramentas integradas (Notion)
├── api/              # Endpoints da API
│   ├── routes.py     # Rotas principais
│   └── v1/           # Versionamento da API
├── core/             # Configurações centrais
│   ├── config.py     # Configurações da aplicação
│   └── logger.py     # Sistema de logging
├── db/               # Camada de banco de dados
│   ├── models.py     # Modelos SQLAlchemy
│   └── session.py    # Sessões de banco
├── handlers/         # Lógica de negócio
│   ├── pergunta_handler.py   # Processamento de perguntas
│   └── tickets_handler.py    # Gestão de tickets
└── main.py          # Aplicação FastAPI
```

## 🚀 Como Executar

### Opção 1: Docker (Recomendado)
```bash
# Construir e executar
docker-compose up --build

# A aplicação estará disponível em http://localhost:8000
```

### Opção 2: Execução Direta
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## ⚙️ Configuração

### 1. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de Dados
DATABASE_URL=postgresql+asyncpg://ia_user:secret@localhost/ia_memory

# APIs Externas
GOOGLE_API_KEY=sua_chave_google_api_aqui
NOTION_API_KEY=sua_chave_notion_aqui
NOTION_DATABASE_ID=id_do_banco_notion_aqui

# Modelo IA (opcional)
GEMINI_MODEL_NAME=gemini-1.5-flash
```

### 2. Banco de Dados
O projeto usa PostgreSQL com migrações Alembic:

```bash
# Executar migrações
alembic upgrade head
```

Com Docker, o banco é configurado automaticamente via `docker-compose.yml`.

## 🧪 Testes

### Instalar Dependências de Teste
```bash
pip install pytest pytest-asyncio aiosqlite
```

### Executar Testes
```bash
# Testes funcionais (recomendado)
pytest tests/test_basic.py tests/test_config.py tests/test_logger.py tests/test_handlers.py tests/test_agents.py -v

# Todos os testes
pytest tests/ -v

# Testes específicos
pytest tests/test_basic.py -v
```

### Cobertura de Testes
- ✅ **Modelos de dados** - Validação de estruturas
- ✅ **Configurações** - Variáveis de ambiente
- ✅ **Sistema de logging** - Funcionalidade de logs
- ✅ **Handlers de negócio** - Lógica principal
- ✅ **Agentes de IA** - Integração com Gemini

## 🔌 API Endpoints

### Health Check
```http
GET /
```
Resposta:
```json
{
  "message": "Capitão IA"
}
```

### Fazer Pergunta
```http
POST /api/v1/perguntar
Content-Type: application/json

{
  "cliente_id": 123,
  "pergunta": "Qual é o status do meu ticket?"
}
```

Resposta:
```json
{
  "resposta": "Resposta do agente IA..."
}
```

### Resumo de Tickets
```http
GET /api/v1/resumo_tickets?cliente_id=123
```

Resposta:
```json
{
  "cliente_id": 123,
  "personagem": "Capitão IA",
  "mensagem": "Resumo dos tickets para cliente 123",
  "tipo": "resumo_inicial"
}
```

## 💾 Banco de Dados

### Modelo de Dados
```sql
-- Tabela de histórico de conversas
CREATE TABLE chat_history (
    id UUID PRIMARY KEY,
    session_id VARCHAR NOT NULL,  -- Agrupa mensagens por conversa
    role VARCHAR NOT NULL,        -- 'user' ou 'model'
    content TEXT NOT NULL,        -- Conteúdo da mensagem
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Gestão de Memória
- Cada cliente tem uma `session_id` única
- Últimas 10 mensagens são recuperadas para contexto
- Histórico completo é mantido para auditoria

## 🔧 Desenvolvimento

### Estrutura de Logs
```python
from app.core.logger import get_logger

logger = get_logger(__name__)
logger.info("Mensagem de log")
```

### Adicionando Novas Ferramentas
1. Criar função em `app/agents/tools/`
2. Registrar em `available_tools`
3. Testar integração

### Padrões de Código
- **Async/await** para operações I/O
- **Type hints** em todas as funções
- **Pydantic models** para validação
- **SQLAlchemy async** para banco de dados

## 📈 Monitoramento

### Logs da Aplicação
```bash
# Via Docker
docker-compose logs -f app

# Execução direta
# Logs aparecem no console
```

### Health Check
```bash
curl http://localhost:8000/
```

## 🤝 Contribuição

1. Fazer fork do projeto
2. Criar branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Abrir Pull Request

## 🆘 Suporte

Para dúvidas ou problemas:
1. Verificar logs da aplicação
2. Validar variáveis de ambiente
3. Executar testes para diagnóstico
4. Abrir issue no repositório

---

**Versão:** 0.1.0  
**Última atualização:** Junho 2025