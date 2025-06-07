from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class Video(BaseModel):
    """Extended video model with additional information"""
   
    id: str
    title: str
    uploader: Optional[str] = None
    duration: Optional[int] = None
    upload_date: Optional[datetime] = None
    description: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    thumbnail_url: Optional[str] = None
    url: str
   
    is_downloaded: bool = False
    download_path: Optional[str] = None
    download_date: Optional[datetime] = None
    file_size_mb: Optional[float] = None
   
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
   
    def format_duration(self) -> str:
        """Formats duration to readable format"""
        if not self.duration:
            return "Unknown"
       
        hours = self.duration // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60
       
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
   
    def format_view_count(self) -> str:
        """Formats view count"""
        if not self.view_count:
            return "Unknown"
       
        if self.view_count >= 1_000_000:
            return f"{self.view_count / 1_000_000:.1f}M views"
        elif self.view_count >= 1_000:
            return f"{self.view_count / 1_000:.1f}K views"
        else:
            return f"{self.view_count} views"
   
    def get_safe_filename(self) -> str:
        """Returns safe filename"""
        invalid_chars = '<>:"/\\|?*'
        safe_title = self.title
        for char in invalid_chars:
            safe_title = safe_title.replace(char, '_')
       
        return safe_title.strip()
   
    def mark_as_downloaded(self, file_path: str, file_size_mb: float = None) -> None:
        """Marks video as downloaded"""
        self.is_downloaded = True
        self.download_path = file_path
        self.download_date = datetime.now()
        self.file_size_mb = file_size_mb
   
    def get_download_info(self) -> Dict[str, Any]:
        """Returns download information"""
        return {
            'is_downloaded': self.is_downloaded,
            'download_path': self.download_path,
            'download_date': self.download_date,
            'file_size_mb': self.file_size_mb
        }