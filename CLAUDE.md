# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Using Docker Compose (recommended)
docker-compose up --build

# Direct Python execution
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Database Setup
The application uses PostgreSQL with SQLAlchemy. Database configuration is handled through docker-compose.yml:
- Database: `ia_memory`
- User: `ia_user` 
- Password: `secret`

### Environment Variables
Create a `.env` file with:
```
DATABASE_URL=postgresql+asyncpg://ia_user:secret@db/ia_memory
GOOGLE_API_KEY=your_google_api_key_here
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_notion_database_id_here
```

### Testing
Run tests with pytest:
```bash
# Install test dependencies
pip install pytest pytest-asyncio aiosqlite

# Run all tests
pytest

# Run specific test files
pytest tests/test_basic.py -v

# Run tests with coverage (optional)
pytest --cov=app tests/
```

Test Structure:
- `tests/test_basic.py`: Basic functionality tests
- `tests/test_config.py`: Configuration tests
- `tests/test_logger.py`: Logging system tests
- `tests/test_handlers.py`: Business logic tests
- `tests/test_agents.py`: AI agent functionality tests

## Architecture Overview

This is an AI Agent system with memory capabilities built on FastAPI and PostgreSQL.

### Core Components

**Agent Layer** (`app/agent/`):
- `core.py`: Main message processing logic that coordinates LLM calls and memory operations
- `memory.py`: Handles conversation history storage and context retrieval (last 5 messages per client)
- `config.py`: Agent configuration (currently empty)

**LLM Layer** (`app/llm/`):
- `base.py`: Abstract base class defining the LLM provider interface
- `google_provider.py`: Google Gemini implementation using `gemini-1.5-flash`
- `openai_provider.py`: OpenAI provider stub (empty)

**Database Layer** (`app/db/`):
- `models.py`: SQLAlchemy model for `Mensagem` (conversation messages)
- `database.py`: Database configuration and session management (empty)

**API Layer** (`app/api/`):
- `routes.py`: FastAPI routes (currently empty)
- `main.py`: FastAPI application entry point with basic health check

### Key Architectural Patterns

1. **Provider Pattern**: LLM providers implement the `LLMProvider` interface, enabling easy switching between different AI models
2. **Memory Management**: Each client gets isolated conversation history with automatic context retrieval
3. **Layered Architecture**: Clear separation between agent logic, LLM providers, database operations, and API routes

### Data Flow
1. Message received → `processar_mensagem()` in `core.py`
2. Context retrieved from database via `recuperar_contexto()`
3. LLM generates response using Google Gemini
4. Conversation saved to database via `salvar_historico()`

### Dependencies
- FastAPI for web framework
- SQLAlchemy + PostgreSQL for persistence
- Google Generative AI for LLM capabilities
- Pydantic for data validation
- Alembic for database migrations