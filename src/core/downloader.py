import os
import sys
import logging
from typing import Dict, Any
from pathlib import Path
import yt_dlp


class AudioDownloader:
    """Main class for audio downloading"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get('output_directory', 'downloads'))
        self.logger = logging.getLogger(__name__)
        self._setup_output_directory()
        
    def _setup_output_directory(self) -> None:
        """Creates output directory if it doesn't exist"""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Output directory ready: {self.output_dir}")
        except OSError as e:
            self.logger.error(f"Failed to create output directory {self.output_dir}: {e}")
            raise

    def _configure_ydl_options(self, dry_run: bool = False) -> Dict[str, Any]:
        """Configures yt-dlp options"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': self.config.get('audio_quality', '320k'),
            'outtmpl': str(self.output_dir / self.config.get('output_filename_template', '%(title)s.%(ext)s')),
            'ignoreerrors': True,
            'simulate': dry_run,
            'verbose': False,
            'quiet': True if dry_run else not self.config.get('display_progress_bar', True),
            'noprogress': True if dry_run else not self.config.get('display_progress_bar', True),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': self.config.get('audio_quality', '320k').replace('k', ''),
            }],
        }

        if self.config.get('skip_downloaded', True):
            ydl_opts['download_archive'] = str(self.output_dir / 'downloaded_archive.txt')

        if self.config.get('proxy_url'):
            ydl_opts['proxy'] = self.config['proxy_url']

        self._configure_playlist_range(ydl_opts)
        
        self._configure_postprocessors(ydl_opts)
        
        if not dry_run and self.config.get('display_progress_bar', True):
            ydl_opts['progress_hooks'] = [self._progress_hook]

        return ydl_opts
    
    def _configure_playlist_range(self, ydl_opts: Dict[str, Any]) -> None:
        """Configures playlist items range"""
        start_idx = self.config.get('download_start_index')
        end_idx = self.config.get('download_end_index')
        
        if start_idx is not None or end_idx is not None:
            range_str = f"{start_idx or 1}:{end_idx or ''}"
            ydl_opts['playlist_items'] = range_str
    
    def _configure_postprocessors(self, ydl_opts: Dict[str, Any]) -> None:
        """Configures postprocessors"""
        if self.config.get('embed_thumbnail', False):
            ydl_opts['postprocessors'].append({
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False
            })

        if self.config.get('add_metadata', True):
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegMetadata'
            })
    
    def _progress_hook(self, d: Dict[str, Any]) -> None:
        """Hook for displaying progress"""
        if d['status'] == 'downloading':
            filename = Path(d.get('filename', '')).name
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', '')
            eta = d.get('_eta_str', '')
            
            sys.stdout.write(f"\r🎵 {filename} - {percent} ({speed}) ETA: {eta}")
            sys.stdout.flush()
        elif d['status'] == 'finished':
            filename = Path(d.get('filename', '')).name
            print(f"\n✅ Completed: {filename}")

    def download(self, url: str) -> bool:
        """
        Downloads audio by URL
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"Starting download: {url}")
        ydl_opts = self._configure_ydl_options(dry_run=False)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                self.logger.info("Download completed successfully!")
                return True
        except yt_dlp.utils.DownloadError as e:
            self.logger.error(f"Download failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during download: {e}")
            return False
