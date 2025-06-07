from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class VideoInfo(BaseModel):
    """Video information model"""
    id: str
    title: str
    duration: Optional[int] = None
    uploader: Optional[str] = None
    upload_date: Optional[datetime] = None
    url: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }    
        
    def get_total_duration(self) -> int:
        """Returns total playlist duration in seconds"""
        return sum(video.duration or 0 for video in self.videos)

    def get_formatted_duration(self) -> str:
        """Returns formatted total duration"""
        total_seconds = self.get_total_duration()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
       
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"


class PlaylistInfo(BaseModel):
    """Playlist information model"""
    id: str
    title: str
    uploader: Optional[str] = None
    description: Optional[str] = None
    video_count: int = Field(ge=0)
    videos: List[VideoInfo] = Field(default_factory=list)
    url: str
    
    def get_total_duration(self) -> int:
        """Returns total playlist duration in seconds"""
        return sum(video.duration or 0 for video in self.videos)
   
    def get_formatted_duration(self) -> str:
        """Returns formatted total duration"""
        total_seconds = self.get_total_duration()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
       
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
   
    def get_videos_by_uploader(self, uploader: str) -> List[VideoInfo]:
        """Returns videos by specific uploader"""
        return [video for video in self.videos if video.uploader == uploader]