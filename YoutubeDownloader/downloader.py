import os
import sys
import re
from urllib.parse import urlparse, parse_qs
from PyQt6.QtCore import QObject, pyqtSignal
from yt_dlp import YoutubeDL

def clean_youtube_url(url):
    """
    Clean YouTube URL by extracting just the video ID and creating a clean URL.
    Handles both youtube.com and youtu.be formats.
    """
    if not url:
        return url
        
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Handle youtu.be format
    if parsed_url.netloc == 'youtu.be':
        video_id = parsed_url.path.lstrip('/')
        return f"https://www.youtube.com/watch?v={video_id}"
    
    # Handle youtube.com format
    elif 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [''])[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
    
    # If we couldn't parse it, return the original URL
    return url

class DownloadWorker(QObject):
    """Worker class to handle YouTube downloads in a separate thread."""
    progress_changed = pyqtSignal(str, float, dict)  # url, progress percentage, info_dict
    download_finished = pyqtSignal(str, bool, str)  # url, success, message
    
    def __init__(self):
        super().__init__()
        self.is_cancelled = False
    
    def download_video(self, url):
        """Download a YouTube video and emit progress signals."""
        try:
            # Clean the URL to remove unnecessary parameters
            clean_url = clean_youtube_url(url)
            
            ydl_opts = {
                'format': 'bestvideo[height<=1081]+bestaudio/best[height<=1080]',
                'outtmpl': '%(title)s.%(ext)s',
                'progress_hooks': [self._progress_hook],
                'quiet': True,  # Suppress console output
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                # First get info to have the title before download starts
                info_dict = ydl.extract_info(clean_url, download=False)
                if self.is_cancelled:
                    self.download_finished.emit(url, False, "Download cancelled")
                    return
                
                # Then download
                ydl.download([clean_url])
                
            self.download_finished.emit(url, True, f"Successfully downloaded: {info_dict.get('title', url)}")
        
        except Exception as e:
            self.download_finished.emit(url, False, f"Error: {str(e)}")
    
    def _progress_hook(self, d):
        """Progress hook for yt-dlp to track download progress."""
        if self.is_cancelled:
            raise Exception("Download cancelled")
            
        if d['status'] == 'downloading':
            # Calculate progress percentage
            total_bytes = d.get('total_bytes')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            if total_bytes is None:
                total_bytes = d.get('total_bytes_estimate', 0)
            
            if total_bytes > 0:
                progress = (downloaded_bytes / total_bytes) * 100
            else:
                progress = 0.0
                
            # Emit the progress signal with the URL and progress percentage
            self.progress_changed.emit(d['info_dict']['webpage_url'], progress, d['info_dict'])
    
    def cancel(self):
        """Cancel the current download."""
        self.is_cancelled = True
