import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional


class FileService:
    """Service for working with files (e.g., saving metadata, logs)"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def save_metadata(self, metadata: Dict[str, Any], file_path: Path) -> bool:
        """
        Saves metadata to JSON file.

        Args:
            metadata: Dictionary with metadata.
            file_path: Path to file where metadata will be saved.

        Returns:
            True if save is successful, False otherwise.
        """
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Metadata saved to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving metadata to {file_path}: {e}")
            return False

    def load_metadata(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Loads metadata from JSON file.

        Args:
            file_path: Path to metadata file.

        Returns:
            Dictionary with metadata if file exists and is successfully read, None otherwise.
        """
        if not file_path.exists():
            self.logger.debug(f"Metadata file not found: {file_path}")
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            self.logger.info(f"Metadata loaded from {file_path}")
            return metadata
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {file_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading metadata from {file_path}: {e}")
            return None

    def write_to_log(self, log_message: str, log_file_path: Path) -> bool:
        """
        Writes message to log file.

        Args:
            log_message: Message to write to log.
            log_file_path: Path to log file.

        Returns:
            True if write is successful, False otherwise.
        """
        try:
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(f"{log_message}\n")
            return True
        except Exception as e:
            self.logger.error(f"Error writing to log file {log_file_path}: {e}")
            return False

    def check_file_exists(self, file_path: Path) -> bool:
        """
        Checks if file exists.

        Args:
            file_path: Path to file.

        Returns:
            True if file exists, False otherwise.
        """
        return file_path.exists()