import pytest
from unittest.mock import patch
import os
from app.core.config import Settings

def test_settings_default_values():
    """Test default values in Settings."""
    with patch.dict(os.environ, {
        'DATABASE_URL': 'postgresql://test:test@localhost/test',
        'GOOGLE_API_KEY': 'test_key',
        'NOTION_API_KEY': 'notion_key',
        'NOTION_DATABASE_ID': 'notion_db_id'
    }):
        settings = Settings()
        assert settings.GEMINI_MODEL_NAME == "gemini-1.5-flash"
        assert settings.DATABASE_URL == 'postgresql://test:test@localhost/test'
        assert settings.GOOGLE_API_KEY == 'test_key'
        assert settings.NOTION_API_KEY == 'notion_key'
        assert settings.NOTION_DATABASE_ID == 'notion_db_id'

def test_settings_override_gemini_model():
    """Test overriding GEMINI_MODEL_NAME."""
    with patch.dict(os.environ, {
        'DATABASE_URL': 'postgresql://test:test@localhost/test',
        'GOOGLE_API_KEY': 'test_key',
        'NOTION_API_KEY': 'notion_key',
        'NOTION_DATABASE_ID': 'notion_db_id',
        'GEMINI_MODEL_NAME': 'gemini-1.5-pro'
    }):
        settings = Settings()
        assert settings.GEMINI_MODEL_NAME == "gemini-1.5-pro"