"""Configuration management for the booking system."""
import os
import sys
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv


@dataclass
class Config:
    """Application configuration."""
    telegram_bot_token: str
    telegram_chat_id: str
    user_email: str
    user_password: str
    target_categories: List[str]
    refresh_interval: int
    headless: bool
    test_mode: bool
    log_level: str = "INFO"

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from environment variables and .env file."""
        # Load .env file if it exists
        load_dotenv()

        # Read configuration values
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        user_email = os.getenv("USER_EMAIL", "")
        user_password = os.getenv("USER_PASSWORD", "")
        
        # Parse target categories
        categories_str = os.getenv("TARGET_CATEGORIES", "")
        target_categories = [cat.strip() for cat in categories_str.split(",") if cat.strip()]
        
        # Parse refresh interval
        try:
            refresh_interval = int(os.getenv("REFRESH_INTERVAL", "5"))
        except ValueError:
            refresh_interval = 5
        
        # Parse boolean values
        headless = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
        test_mode = os.getenv("TEST_MODE", "false").lower() in ("true", "1", "yes")
        
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        config = cls(
            telegram_bot_token=telegram_bot_token,
            telegram_chat_id=telegram_chat_id,
            user_email=user_email,
            user_password=user_password,
            target_categories=target_categories,
            refresh_interval=refresh_interval,
            headless=headless,
            test_mode=test_mode,
            log_level=log_level,
        )
        
        return config

    def validate(self) -> None:
        """Validate configuration and raise errors for invalid values."""
        errors = []

        # Check required credentials
        if not self.telegram_bot_token:
            errors.append("TELEGRAM_BOT_TOKEN is required")
        
        if not self.telegram_chat_id:
            errors.append("TELEGRAM_CHAT_ID is required")
        
        if not self.user_email:
            errors.append("USER_EMAIL is required")
        
        if not self.user_password:
            errors.append("USER_PASSWORD is required")

        # Check target categories
        # Based on actual HTML structure, valid categories are:
        valid_categories = [
            "普通車ＡＭ",
            "普通車ＰＭ",
            "準中型車ＡＭ",
            "準中型車ＰＭ",
            "大型車ＡＭ",
            "大型車ＰＭ",
            "大型特殊車ＡＭ",
            "大型特殊車ＰＭ",
            "けん引車ＡＭ",
            "けん引車ＰＭ",
            "大型二輪車ＡＭ",
            "大型二輪車ＰＭ",
        ]
        
        if not self.target_categories:
            errors.append("TARGET_CATEGORIES is required (at least one category)")
        else:
            for category in self.target_categories:
                if category not in valid_categories:
                    errors.append(
                        f"Invalid category: {category}. "
                        f"Valid categories: {', '.join(valid_categories)}"
                    )

        # Check refresh interval
        if self.refresh_interval < 1:
            errors.append("REFRESH_INTERVAL must be at least 1 second")

        # Check log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level not in valid_log_levels:
            errors.append(f"Invalid LOG_LEVEL: {self.log_level}. Valid levels: {', '.join(valid_log_levels)}")

        if errors:
            error_message = "Configuration errors:\n" + "\n".join(f"  - {error}" for error in errors)
            print(error_message, file=sys.stderr)
            sys.exit(1)
