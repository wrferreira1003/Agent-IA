# app/core/logger.py
import logging
import sys
from logging import Formatter, StreamHandler, Logger

# --- Configurações de Formato de Log ---
# Define um formato padrão para os logs, incluindo timestamp, nome do logger,
# nível do log e a mensagem. Este formato estruturado facilita a leitura e o parsing.
LOG_FORMAT = "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"

# --- Função de Configuração Principal ---
def setup_logging(level: int = logging.INFO):
    """
    Configura o sistema de logging para a aplicação.

    Esta função centraliza a configuração do logger root. Ela define o nível
    de severidade dos logs a serem capturados, cria um handler para enviar os
    logs para o console (stdout) e aplica o formato definido.

    Deve ser chamada apenas uma vez, no início do ciclo de vida da aplicação
    (ex: no `lifespan` do FastAPI), para garantir uma configuração consistente.

    Args:
        level (int, optional): O nível mínimo de log a ser processado.
                               Defaults to logging.INFO.
    """
    # Obtém o logger raiz da hierarquia de loggers.
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Verifica se já existem handlers configurados para evitar duplicação de logs
    # caso esta função seja acidentalmente chamada mais de uma vez.
    if not root_logger.handlers:
        # Cria um handler para direcionar os logs para a saída padrão (console).
        console_handler = StreamHandler(sys.stdout)
        
        # Cria um formatador com o padrão de log definido.
        formatter = Formatter(LOG_FORMAT)
        
        # Associa o formatador ao handler.
        console_handler.setFormatter(formatter)
        
        # Adiciona o handler configurado ao logger raiz.
        root_logger.addHandler(console_handler)
        
        root_logger.info("Sistema de logging configurado com sucesso.")

    # --- Configuração Padrão para Bibliotecas Externas ---
    # Reduz o "ruído" de bibliotecas comuns, mostrando apenas logs de aviso (WARNING)
    # ou mais graves. Isso limpa a saída de log, focando nas mensagens da nossa aplicação.
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    # Exemplo: descomente a linha abaixo para ver mais detalhes de uma biblioteca específica.
    # logging.getLogger("notion_client").setLevel(logging.INFO)

# --- Função Auxiliar para Obter Loggers ---
def get_logger(name: str) -> Logger:
    """
    Função auxiliar para obter uma instância de logger nomeada.

    É a forma recomendada para obter um logger em qualquer módulo da aplicação.
    Usar `__name__` como argumento cria um logger com o nome do próprio módulo,
    o que ajuda a identificar a origem das mensagens de log.

    Args:
        name (str): O nome para o logger (geralmente `__name__`).

    Returns:
        Logger: Uma instância de logger pronta para uso.
    """
    return logging.getLogger(name)
