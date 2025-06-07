import logging
from typing import Optional, Dict, Any, Tuple
from ..core.downloader import AudioDownloader
from ..core.extractor import InfoExtractor
from ..core.validator import URLValidator
from ..models.playlist import PlaylistInfo
from ..models.video import Video


class YouTubeService:
    """Service for working with YouTube"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.downloader = AudioDownloader(config)
        self.extractor = InfoExtractor(config)
        self.validator = URLValidator()
        self.logger = logging.getLogger(__name__)

    def validate_url(self, url: str) -> Tuple[bool, str]:
        """
        Validates YouTube URL

        Args:
            url: URL to check

        Returns:
            Tuple (is_valid, message)
        """
        if not self.validator.is_valid_url(url):
            return False, "Invalid URL format"

        if not self.validator.is_youtube_url(url):
            return False, "Not a YouTube URL"

        url_type = self.validator.get_url_type(url)
        if url_type == 'unknown':
            return False, "Unsupported YouTube URL type"

        return True, ""

    def get_playlist_info(self, url: str) -> Optional[PlaylistInfo]:
        """
        Extracts playlist information

        Args:
            url: Playlist URL

        Returns:
            PlaylistInfo or None on error
        """
        return self.extractor.extract_playlist_info(url)

    def download_playlist(self, url: str) -> bool:
        """
        Downloads audio from playlist

        Args:
            url: Playlist URL

        Returns:
            True if successful, False otherwise
        """
        return self.downloader.download(url)

    def get_video_info(self, url: str) -> Optional[Video]:
        """
        Extracts information about a single video

        Args:
            url: Video URL

        Returns:
            Video or None on error
        """
        video_info = self.extractor.extract_video_info(url)
        if not video_info:
            return None

        video = Video(
            id=video_info.id,
            title=video_info.title,
            uploader=video_info.uploader,
            duration=video_info.duration,
            upload_date=video_info.upload_date,
            url=video_info.url
        )
        return video