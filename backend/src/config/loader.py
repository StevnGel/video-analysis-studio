"""Configuration loader for app.yaml"""

import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ModelPoolConfig(BaseSettings):
    gpu_instances: list = []
    instance_timeout: int = 300
    max_queue_size: int = 100


class ServerConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    reload: bool = True


class StorageConfig(BaseSettings):
    video_dir: str = "/data/videos"
    output_dir: str = "/data/output"
    archive_dir: str = "/data/archive"


class TaskConfig(BaseSettings):
    default_timeout: int = 3600
    max_concurrent_tasks: int = 10
    auto_restart: bool = True


class LoggingConfig(BaseSettings):
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class AppConfig(BaseSettings):
    name: str = "video-analysis-studio"
    version: str = "1.0.0"
    environment: str = "development"


class Settings(BaseSettings):
    app: AppConfig = AppConfig()
    server: ServerConfig = ServerConfig()
    model_pool: ModelPoolConfig = ModelPoolConfig()
    task: TaskConfig = TaskConfig()
    storage: StorageConfig = StorageConfig()
    logging: LoggingConfig = LoggingConfig()
    models: Dict[str, Any] = {}

    class Config:
        env_file = ".env"


class ConfigLoader:
    """Configuration loader with environment variable substitution"""

    PLACEHOLDER_PATTERN = re.compile(r"\$\{([^}]+)}")

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            base_dir = Path(__file__).parent.parent.parent
            config_path = base_dir / "config" / "app.yaml"
        self.config_path = Path(config_path)
        self._settings: Optional[Settings] = None
        self._raw_config: Dict[str, Any] = {}

    def load(self) -> Settings:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            return Settings()

        with open(self.config_path, "r") as f:
            self._raw_config = yaml.safe_load(f) or {}

        config_dict = self._resolve_env_vars(self._raw_config)
        self._settings = Settings(**config_dict)
        return self._settings

    def _resolve_env_vars(self, config: Any) -> Any:
        """Resolve environment variable references ${VAR}"""
        if isinstance(config, str):
            def replace_env_var(match):
                var_name = match.group(1)
                return os.getenv(var_name, match.group(0))
            return self.PLACEHOLDER_PATTERN.sub(replace_env_var, config)
        elif isinstance(config, dict):
            return {k: self._resolve_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._resolve_env_vars(item) for item in config]
        return config

    def resolve_placeholders(self, template: str, variables: Dict[str, str]) -> str:
        """Resolve template placeholders with provided variables"""
        def replace_placeholder(match):
            key = match.group(1)
            return variables.get(key, match.group(0))
        return self.PLACEHOLDER_PATTERN.sub(replace_placeholder, template)

    @property
    def settings(self) -> Settings:
        """Get loaded settings"""
        if self._settings is None:
            self.load()
        return self._settings


_settings_instance: Optional[ConfigLoader] = None


def get_settings() -> Settings:
    """Get global settings instance"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = ConfigLoader()
        _settings_instance.load()
    return _settings_instance.settings