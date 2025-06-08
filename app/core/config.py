from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Carrega e valida as configurações da aplicação a partir de variáveis de ambiente.
    """
    # Carrega variáveis do arquivo .env
    model_config = SettingsConfigDict(env_file="app/.env", env_file_encoding='utf-8', extra='ignore')

    # Configurações do Banco de Dados
    DATABASE_URL: str

    # Chaves de API
    GOOGLE_API_KEY: str
    NOTION_API_KEY: str
    NOTION_DATABASE_ID: str # Exemplo: ID do banco de dados do Notion para consultas

    # Configurações do Modelo
    GEMINI_MODEL_NAME: str = "gemini-1.5-flash"

# Instância única das configurações para ser importada em toda a aplicação
settings = Settings()