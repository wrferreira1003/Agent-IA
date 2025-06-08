import pytest
import logging
from unittest.mock import patch, Mock
from app.core.logger import setup_logging, get_logger

def test_setup_logging():
    """Test logger setup function."""
    # Clear existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    setup_logging(level=logging.DEBUG)
    
    assert root_logger.level == logging.DEBUG
    assert len(root_logger.handlers) > 0
    
    # Verificar se não adiciona handlers duplicados
    initial_handler_count = len(root_logger.handlers)
    setup_logging(level=logging.INFO)
    assert len(root_logger.handlers) == initial_handler_count

def test_get_logger():
    """Test get_logger function."""
    logger = get_logger("test_module")
    
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_module"

def test_logging_external_libraries():
    """Test that external library logging levels are set correctly."""
    setup_logging()
    
    uvicorn_logger = logging.getLogger("uvicorn")
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    
    assert uvicorn_logger.level == logging.WARNING
    assert sqlalchemy_logger.level == logging.WARNING