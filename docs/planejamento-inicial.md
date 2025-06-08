## 📆 Planejamento Detalhado de Desenvolvimento do Serviço de IA com SDK do Google

### 🌟 Visão Geral do Projeto

Criaremos um serviço de IA autônomo e modular utilizando o SDK oficial do Google (Google Generative AI), com base em FastAPI (Python) e PostgreSQL, integrando memória persistente e contexto via documentos do Notion. O projeto é arquitetado desde o início para permitir:

* Integração futura com backend Go ou frontend web/mobile.
* Suporte a múltiplos modelos LLM (Gemini, OpenAI, Mistral, etc.).
* Experiência de onboarding com agente/personagem virtual.

---

### 💡 Fase 1: Criação do Projeto e Ambiente

**Objetivo:** Estabelecer a base do projeto com estrutura de diretórios, ambiente Python e containerização.

#### Etapas:

1. Criar diretório raiz do projeto:

   ```bash
   mkdir ia-agent-service && cd ia-agent-service
   ```

2. Estrutura de pastas inicial:

   ```bash
   .
   ├── app/
   │   ├── main.py
   │   ├── api/routes.py
   │   ├── agent/core.py
   │   ├── agent/memory.py
   │   ├── agent/context_loader.py
   │   ├── agent/config.py
   │   ├── db/database.py
   │   ├── db/models.py
   │   ├── llm/base.py
   │   ├── llm/google_provider.py
   │   ├── llm/openai_provider.py (placeholder)
   │   └── utils/formatter.py
   ├── alembic/
   ├── requirements.txt
   ├── .env
   ├── Dockerfile
   └── docker-compose.yml
   ```

3. Criar ambiente virtual e instalar dependências:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary httpx python-dotenv google-generativeai notion-client
   pip freeze > requirements.txt
   ```

4. Dockerfile e docker-compose configurados para subir o FastAPI + PostgreSQL.

5. Configuração do SDK do Google via `.env`:

   ```dotenv
   GOOGLE_API_KEY=xxxx
   LLM_PROVIDER=google
   NOTION_API_KEY=xxxx
   DATABASE_URL=postgresql://ia_user:secret@db:5432/ia_memory
   ```

---

### 🔄 Fase 2: Implementação do Agente IA

**Objetivo:** Criar o agente principal com capacidade de:

* Receber pergunta via API,
* Consultar contexto (memória + Notion),
* Gerar resposta com base na LLM (Google Gemini).

#### Etapas:

1. Definir interface `LLMProvider` (`base.py`) para suporte a múltiplos provedores.
2. Implementar `GoogleProvider` com SDK oficial.
3. Utilizar o ambiente de testes interativo do SDK via Makersuite ou lib Python.
4. Criar `core.py` com lógica de integração entre entrada → memória → contexto → resposta → gravação.

---

### 📊 Fase 3: Banco de Dados e Memória Persistente

**Objetivo:** Permitir que o agente tenha memória real e contextual.

#### Etapas:

1. Criar modelos ORM:

   * `mensagem`: pergunta, resposta, cliente\_id, timestamp
   * `sessao`: contexto geral

2. Configurar Alembic para migrações.

3. Desenvolver métodos em `memory.py` para manipulação da memória.

---

### 📚 Fase 4: Integração com Notion para Contexto

**Objetivo:** Carregar documentos de conhecimento via Notion API.

#### Etapas:

1. Criar `context_loader.py`
2. Implementar funções para:

   * Buscar documentos por ID ou tag
   * Extrair e limpar texto
3. Integrar com `core.py` para compor o prompt final.

---

### 🚀 Fase 5: Exposição da API REST

**Objetivo:** Permitir comunicação externa com o serviço.

#### Endpoints principais:

* `POST /perguntar`
* `POST /evento/boasvindas`

#### Exemplo de entrada:

```json
{
  "mensagem": "Qual a garantia da linha A?",
  "cliente_id": 123
}
```

#### Exemplo de resposta:

```json
{
  "resposta": "A linha A possui 12 meses de garantia para uso urbano."
}
```

---

### 💬 Fase 6: Personagem de Onboarding e Boas-Vindas

**Objetivo:** Criar uma experiência interativa com um personagem virtual (ex: Joelizinho).

#### Etapas:

1. Criar prompt base amigável.
2. Modelar entrada com contexto (ex: resumo de tickets).
3. Gerar resposta da IA com sugestões práticas.
4. Exibir no frontend (balão/personagem).

---

### 🔌 Fase 7: Suporte a Múltiplas LLMs (Modularização)

**Objetivo:** Permitir alternância entre diferentes provedores de IA.

#### Etapas:

1. Interface `LLMProvider` já definida.
2. Adicionar outros adaptadores (OpenAI, Ollama, Mistral).
3. Selecionar via `.env`:

   ```dotenv
   LLM_PROVIDER=google
   ```

---

### 🧪 Fase 8: Testes Automatizados e Logs

**Objetivo:** Garantir qualidade e rastreabilidade.

#### Etapas:

* Escrever testes unitários (Pytest)
* Implementar logging estruturado
* Criar script de health check

---

### 🏁 Fase 9: Preparação para Produção

**Objetivo:** Garantir operação estável em ambiente real.

#### Etapas:

* Configurar HTTPS e tokens de acesso
* Adicionar rate limiting
* Deploy via Docker/Kubernetes
* Pipeline CI/CD com GitHub Actions

---

### 🎉 Finalização

Com esse planejamento, temos um serviço pronto para rodar isolado ou integrado, com suporte à IA contextual, agentes com memória, múltiplas LLMs, e uma base sólida para escalar com segurança e performance.
