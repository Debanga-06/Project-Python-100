"""
Bot configuration settings.
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BotConfig:
    # Timing
    WAIT_TIMEOUT: int = 15           # seconds to wait for elements
    PAGE_LOAD_DELAY: float = 1.5     # delay after page navigation
    TYPING_DELAY: float = 0.03       # delay between keystrokes
    ACTION_DELAY: float = 0.8        # general delay between actions

    # Retry
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 2.0

    # Paths
    SCREENSHOTS_DIR: str = "screenshots"
    LOGS_DIR: str = "logs"
    DATA_DIR: str = "data"

    # Optional credentials (load from .env)
    GITHUB_USERNAME: str = field(default_factory=lambda: os.getenv("GITHUB_USERNAME", ""))
    GITHUB_PASSWORD: str = field(default_factory=lambda: os.getenv("GITHUB_PASSWORD", ""))

    LINKEDIN_EMAIL: str = field(default_factory=lambda: os.getenv("LINKEDIN_EMAIL", ""))
    LINKEDIN_PASSWORD: str = field(default_factory=lambda: os.getenv("LINKEDIN_PASSWORD", ""))

    REDDIT_USERNAME: str = field(default_factory=lambda: os.getenv("REDDIT_USERNAME", ""))
    REDDIT_PASSWORD: str = field(default_factory=lambda: os.getenv("REDDIT_PASSWORD", ""))


# Global config instance
config = BotConfig()
