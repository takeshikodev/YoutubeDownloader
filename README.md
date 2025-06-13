# YoutubeDownloader

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Overview

**YoutubeDownloader** is a Python application that allows users to download music and playlists from YouTube. The tool provides a user-friendly command-line interface with rich text formatting, making it easy to download your favorite music content. It's built with a clean architecture that separates business logic from technical implementations and provides a flexible configuration system.

### Target Audience
- Music enthusiasts
- Content creators
- Users who want to save YouTube audio for offline listening
- Anyone who needs to archive YouTube audio content

## Features

### Download Capabilities

- **Video Download**: Download individual YouTube videos as audio files
- **Playlist Support**: Download entire YouTube playlists
- **Audio Extraction**: Automatically extracts audio from videos
- **Format Conversion**: Converts to MP3 format with configurable quality
- **Metadata Handling**: Preserves and adds metadata to downloaded files

### User Experience

- **Rich CLI Interface**: Beautiful command-line interface with colors and formatting
- **Progress Tracking**: Real-time download progress display
- **Configuration Management**: Interactive configuration setup
- **Proxy Support**: Optional proxy configuration for network restrictions
- **Customizable Output**: Control naming patterns and output location

### Advanced Options

- **Download Filtering**: Select specific videos from playlists
- **Quality Control**: Configure audio quality settings
- **Thumbnail Embedding**: Option to embed video thumbnails in audio files
- **Skip Downloaded**: Avoid re-downloading previously downloaded content
- **Error Handling**: Robust error handling and logging

## Technologies

- **Python**: Primary programming language
- **yt-dlp**: Core YouTube download functionality
- **Rich**: Terminal formatting and user interface
- **FFmpeg**: Audio processing and conversion
- **Pydantic**: Data validation and configuration management
- **Logging**: Comprehensive logging system

## Architecture

YoutubeDownloader follows a modular architecture with clear separation of concerns:

1. **Core Layer**: Contains the essential business logic
   - `downloader.py`: Handles the actual download process
   - `extractor.py`: Extracts information from YouTube URLs
   - `validator.py`: Validates URLs and input parameters

2. **Models Layer**: Defines data structures
   - `playlist.py`: Playlist information model
   - `video.py`: Video information model

3. **Services Layer**: Coordinates between components
   - `youtube_service.py`: Manages YouTube-related operations
   - `file_service.py`: Handles file system operations

4. **UI Layer**: User interaction
   - `cli.py`: Command-line interface implementation
   - `prompts.py`: User interaction prompts and messages

5. **Config Layer**: Configuration management
   - `config_manager.py`: Manages application configuration

## Installation

### Prerequisites

- Python 3.8+
- FFmpeg (required for audio conversion)

### Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/takeshikodev/YoutubeDownloader.git
   cd YoutubeDownloader
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg:**
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` or equivalent

## Configuration

Configuration is managed through `config.json` in the project root:

```json
{
  "output_directory": "output_directory",
  "proxy_url": "http://user:password@host:port",
  "audio_quality": "320k",
  "log_level": "INFO",
  "skip_downloaded": true,
  "download_start_index": null,
  "download_end_index": null,
  "max_downloads": null,
  "output_filename_template": "%(playlist_index)s - %(title)s.%(ext)s",
  "embed_thumbnail": false,
  "add_metadata": true,
  "sleep_interval_between_videos": 0,
  "force_overwrites": false,
  "display_progress_bar": true
}
```

### Configuration Parameters

- **output_directory**: Directory where downloaded files will be saved
- **proxy_url**: Optional HTTP/SOCKS proxy for connections
- **audio_quality**: Audio quality (e.g., "128k", "320k")
- **log_level**: Logging level (INFO, DEBUG, WARNING, ERROR)
- **skip_downloaded**: Whether to skip already downloaded files
- **download_start_index**: Starting index for playlist downloads
- **download_end_index**: Ending index for playlist downloads
- **output_filename_template**: Template for output filenames
- **embed_thumbnail**: Whether to embed video thumbnails in audio files
- **add_metadata**: Whether to add metadata to audio files
- **display_progress_bar**: Whether to show download progress

## Usage

Run the application using:

```bash
python main.py
```

Follow the interactive prompts to:
1. Configure download settings
2. Enter a YouTube URL (video or playlist)
3. Review information about the content
4. Confirm and start download

## Project Structure

```
youtubedownloader/
├── src/                  # Source code
│   ├── core/             # Core functionality
│   │   ├── downloader.py # Download handling
│   │   ├── extractor.py  # Information extraction
│   │   ├── validator.py  # URL validation
│   │   └── __init__.py   # Package initialization
│   ├── models/           # Data models
│   │   ├── playlist.py   # Playlist model
│   │   ├── video.py      # Video model
│   │   └── __init__.py   # Package initialization
│   ├── services/         # Service layer
│   │   ├── youtube_service.py # YouTube operations
│   │   ├── file_service.py    # File operations
│   │   └── __init__.py        # Package initialization
│   ├── ui/               # User interface
│   │   ├── cli.py        # Command-line interface
│   │   ├── prompts.py    # User prompts
│   │   └── __init__.py   # Package initialization
│   ├── config/           # Configuration
│   │   ├── config_manager.py  # Config management
│   │   └── __init__.py        # Package initialization
│   └── __init__.py       # Package initialization
├── config.json           # Configuration file
├── requirements.txt      # Dependencies
├── LICENSE               # License information
├── README.md             # Documentation
└── main.py               # Entry point
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Takeshiko 
