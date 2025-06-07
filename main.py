#!/usr/bin/env python3
"""
YouTube Music Downloader - Main Entry Point
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from src.ui.cli import CLI


def main():
    """Main entry point"""
    try:
        (project_root / "logs").mkdir(exist_ok=True)

        cli = CLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()