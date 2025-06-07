import re
import logging
from typing import Optional, Tuple
from urllib.parse import urlparse


class URLValidator:
    """URL validator"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)(?:&list=([a-zA-Z0-9_-]+))?',
            r'(?:https?://)?youtu\.be/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/channel/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/user/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/c/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?music\.youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)',
        ]
    
    def is_valid_url(self, url: str) -> bool:
        """
        Checks URL validity
        
        Args:
            url: URL to check
            
        Returns:
            True if URL is valid
        """
        if not url or not isinstance(url, str):
            return False
        
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def validate_url(self, url: str) -> Tuple[bool, str]:
        """
        Validates URL and returns result with message
        
        Args:
            url: URL to check
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not url or not isinstance(url, str):
            return False, "URL is empty or not a string"
        
        if not self.is_valid_url(url):
            return False, "Invalid URL format"
        
        if not self.is_youtube_url(url):
            return False, "URL is not a valid YouTube URL"
        
        url_type = self.get_url_type(url)
        if url_type == 'unknown':
            return False, "Unknown YouTube URL type"
        
        return True, f"Valid {url_type} URL"
    
    def is_youtube_url(self, url: str) -> bool:
        """
        Checks if URL is a YouTube link
        
        Args:
            url: URL to check
            
        Returns:
            True if this is a YouTube URL
        """
        if not self.is_valid_url(url):
            return False
        
        youtube_domains = [
            'youtube.com',
            'www.youtube.com',
            'youtu.be',
            'music.youtube.com'
        ]
        
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower() in youtube_domains
        except Exception:
            return False
    
    def is_playlist_url(self, url: str) -> bool:
        """
        Checks if URL is a playlist link
        
        Args:
            url: URL to check
            
        Returns:
            True if this is a playlist URL
        """
        if not self.is_youtube_url(url):
            return False
        
        return 'list=' in url or 'playlist' in url
    
    def extract_playlist_id(self, url: str) -> Optional[str]:
        """
        Extracts playlist ID from URL
        
        Args:
            url: Playlist URL
            
        Returns:
            Playlist ID or None
        """
        for pattern in self.youtube_patterns:
            match = re.search(pattern, url)
            if match:
                groups = match.groups()
                for group in groups:
                    if group and len(group) > 10:
                        return group
        return None
    
    def validate_proxy_url(self, proxy_url: str) -> bool:
        """
        Validates proxy URL
        
        Args:
            proxy_url: Proxy URL to check
            
        Returns:
            True if proxy URL is valid
        """
        if not proxy_url:
            return False
        
        valid_schemes = ['http', 'https', 'socks4', 'socks5']
        
        try:
            parsed = urlparse(proxy_url)
            return parsed.scheme.lower() in valid_schemes and bool(parsed.netloc)
        except Exception:
            return False
    
    def get_url_type(self, url: str) -> str:
        """
        Determines YouTube URL type
        
        Args:
            url: URL to analyze
            
        Returns:
            URL type: 'playlist', 'video', 'channel', 'unknown'
        """
        if not self.is_youtube_url(url):
            return 'unknown'
        
        if 'playlist' in url or 'list=' in url:
            return 'playlist'
        elif 'watch?v=' in url or 'youtu.be/' in url:
            return 'video'
        elif 'channel/' in url or 'user/' in url or '/c/' in url:
            return 'channel'
        
        return 'unknown'