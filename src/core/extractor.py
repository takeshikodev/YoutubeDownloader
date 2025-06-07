import logging
from typing import Optional, Dict, Any
import yt_dlp
from ..models.playlist import PlaylistInfo, VideoInfo


class InfoExtractor:
    """Extracts video and playlist information"""
   
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
   
    def _get_ydl_options(self) -> Dict[str, Any]:
        """Returns options for information extraction"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'simulate': True,
            'extract_flat': False,
        }
       
        if self.config.get('proxy_url'):
            ydl_opts['proxy'] = self.config['proxy_url']
           
        return ydl_opts
   
    def extract_playlist_info(self, url: str) -> Optional[PlaylistInfo]:
        """
        Extracts playlist information
       
        Args:
            url: Playlist URL
           
        Returns:
            PlaylistInfo or None on error
        """
        self.logger.info(f"Extracting playlist info: {url}")
       
        try:
            with yt_dlp.YoutubeDL(self._get_ydl_options()) as ydl:
                info = ydl.extract_info(url, download=False)
               
                if not info:
                    return None
               
                if 'entries' in info:
                    entries = info.get('entries', [])
                    videos = []
                    
                    for entry in entries:
                        if entry:
                            video = VideoInfo(
                                id=entry.get('id', ''),
                                title=entry.get('title', 'Unknown'),
                                duration=entry.get('duration'),
                                uploader=entry.get('uploader'),
                                url=entry.get('webpage_url', entry.get('url', ''))
                            )
                            videos.append(video)
                    
                    playlist = PlaylistInfo(
                        id=info.get('id', ''),
                        title=info.get('title', 'Unknown Playlist'),
                        uploader=info.get('uploader'),
                        description=info.get('description'),
                        video_count=len(videos),
                        videos=videos,
                        url=url
                    )
                    self.logger.info(f"Extracted playlist: {playlist.title} ({len(videos)} videos)")
                    return playlist
                
                else:
                    video = VideoInfo(
                        id=info.get('id', ''),
                        title=info.get('title', 'Unknown'),
                        duration=info.get('duration'),
                        uploader=info.get('uploader'),
                        url=url
                    )
                    self.logger.info(f"Extracted video: {video.title}")
                    
                    return PlaylistInfo(
                        id=video.id,
                        title=video.title,
                        uploader=video.uploader,
                        description="Single video",
                        video_count=1,
                        videos=[video],
                        url=url
                    )
               
        except yt_dlp.utils.DownloadError as e:
            self.logger.error(f"Failed to extract playlist info: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error extracting info: {e}")
            return None
   
    def extract_video_info(self, url: str) -> Optional[VideoInfo]:
        """
        Extracts video information
       
        Args:
            url: Video URL
           
        Returns:
            VideoInfo or None on error
        """
        try:
            with yt_dlp.YoutubeDL(self._get_ydl_options()) as ydl:
                info = ydl.extract_info(url, download=False)
               
                if not info:
                    return None
               
                video = VideoInfo(
                    id=info.get('id', ''),
                    title=info.get('title', 'Unknown'),
                    duration=info.get('duration'),
                    uploader=info.get('uploader'),
                    url=url
                )
               
                return video
               
        except Exception as e:
            self.logger.error(f"Error extracting video info: {e}")
            return None
        