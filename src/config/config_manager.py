import json
import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, validator


class DownloadConfig(BaseModel):
    """Download config"""

    output_directory: str = "downloaded_youtube_music"
    proxy_url: Optional[str] = None
    audio_quality: str = "320k"
    log_level: str = "INFO"
    skip_downloaded: bool = True
    download_start_index: Optional[int] = None
    download_end_index: Optional[int] = None
    max_downloads: Optional[int] = None
    output_filename_template: str = "%(playlist_index)s - %(title)s.%(ext)s"
    embed_thumbnail: bool = False
    add_metadata: bool = True
    sleep_interval_between_videos: int = 0
    force_overwrites: bool = False
    display_progress_bar: bool = True

    @validator('audio_quality')
    def validate_audio_quality(cls, v):
        valid_qualities = ['64k', '128k', '192k', '256k', '320k']
        if v not in valid_qualities:
            raise ValueError(
                f'Invalid audio quality. Must be one of: {valid_qualities}')
        return v

    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(
                f'Invalid log level. Must be one of: {valid_levels}')
        return v.upper()


class ConfigManager:
    """App config manager"""

    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self._config: Optional[DownloadConfig] = None
        self.logger = logging.getLogger(__name__)

    def load_config(self) -> DownloadConfig:
        """Loads config from file"""
        if not self.config_file.exists():
            self.logger.warning(
                f"Config file '{self.config_file}' not found. Creating default config.")
            self._create_default_config()

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            self._config = DownloadConfig(**config_data)
            self.logger.info(f"Configuration loaded from {self.config_file}")
            return self._config

        except json.JSONDecodeError as e:
            self.logger.error(
                f"Error decoding JSON from {self.config_file}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            raise

    def _create_default_config(self):
        """Creates default config"""
        default_config = DownloadConfig()
        self.save_config(default_config)

    def save_config(self, config: DownloadConfig):
        """Saves config to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config.dict(), f, indent=2, ensure_ascii=False)
            self.logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            raise

    @property
    def config(self) -> DownloadConfig:
        """Returns config"""
        if self._config is None:
            self._config = self.load_config()
        return self._config

    def update_config(self, **kwargs) -> None:
        """Updates config"""
        if self._config is None:
            self.load_config()

        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)

        self.save_config(self._config)