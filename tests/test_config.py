"""Tests for configuration management."""
import os
import pytest
from src.config import Config


def test_config_load_with_env_vars(monkeypatch):
    """Test loading configuration from environment variables."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test_chat_id")
    monkeypatch.setenv("TARGET_CATEGORIES", "普通車ＡＭ,普通車ＰＭ")
    monkeypatch.setenv("REFRESH_INTERVAL", "10")
    monkeypatch.setenv("HEADLESS", "true")
    monkeypatch.setenv("TEST_MODE", "false")
    
    config = Config.load()
    
    assert config.telegram_bot_token == "test_token"
    assert config.telegram_chat_id == "test_chat_id"
    assert config.target_categories == ["普通車ＡＭ", "普通車ＰＭ"]
    assert config.refresh_interval == 10
    assert config.headless is True
    assert config.test_mode is False


def test_config_validation_missing_token(monkeypatch):
    """Test validation fails when token is missing."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test_chat_id")
    monkeypatch.setenv("TARGET_CATEGORIES", "普通車ＡＭ")
    
    config = Config.load()
    
    with pytest.raises(SystemExit):
        config.validate()


def test_config_validation_invalid_category(monkeypatch):
    """Test validation fails with invalid category."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test_chat_id")
    monkeypatch.setenv("TARGET_CATEGORIES", "InvalidCategory")
    
    config = Config.load()
    
    with pytest.raises(SystemExit):
        config.validate()


def test_config_validation_success(monkeypatch):
    """Test validation succeeds with valid configuration."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test_chat_id")
    monkeypatch.setenv("TARGET_CATEGORIES", "普通車ＡＭ")
    
    config = Config.load()
    
    # Should not raise
    config.validate()
