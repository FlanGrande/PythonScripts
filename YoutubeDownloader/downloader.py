from urllib.parse import urlparse, parse_qs
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
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
    
    def download_video(self, url, selected_format="mp4"):
        """Download a YouTube video and emit progress signals."""
        try:
            # Clean the URL to remove unnecessary parameters
            clean_url = clean_youtube_url(url)
            
            if selected_format in ["mp3", "ogg", "wav"]:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '%(title)s.%(ext)s',
                    'progress_hooks': [self._progress_hook],
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': selected_format,
                        'preferredquality': '5',
                    }],
                }
            elif selected_format in ["mp4", "webm"]:
                ydl_opts = {
                    'format': 'bestvideo[height<=1081]+bestaudio/best[height<=1080]',
                    'outtmpl': '%(title)s.%(ext)s',
                    'progress_hooks': [self._progress_hook],
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferredformat': selected_format,
                    }],
                }
            else:
                ydl_opts = {
                    'format': 'bestvideo[height<=1081]+bestaudio/best[height<=1080]',
                    'outtmpl': '%(title)s.%(ext)s',
                    'progress_hooks': [self._progress_hook],
                    'quiet': True,
                }
            
            # First get info to have the title before download starts
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(clean_url, download=False)
                
                # Process events after info extraction to keep UI responsive
                QApplication.processEvents()
                
                if self.is_cancelled:
                    self.download_finished.emit(url, False, "Download cancelled")
                    return
                
                # Check if info_dict is valid
                if not info_dict or 'title' not in info_dict:
                    self.download_finished.emit(url, False, "Could not retrieve video information")
                    return
                
                # Then download
                ydl.download([clean_url])
                
                # Process events after download to keep UI responsive
                QApplication.processEvents()
            
            self.download_finished.emit(url, True, f"Successfully downloaded: {info_dict.get('title', url)}")
        
        except Exception as e:
            # Process events before emitting error to keep UI responsive
            QApplication.processEvents()
            error_message = str(e)
            
            # Provide more user-friendly error messages for common errors
            if "Video unavailable" in error_message:
                error_message = "Video is unavailable or private"
            elif "sign in to" in error_message.lower():
                error_message = "This video requires age verification or sign-in"
            elif "copyright" in error_message.lower():
                error_message = "This video has been removed due to copyright issues"
            elif "not exist" in error_message.lower():
                error_message = "The video does not exist or has been removed"
            elif "network" in error_message.lower() or "connection" in error_message.lower():
                error_message = "Network error - Please check your internet connection"
                
            self.download_finished.emit(url, False, f"Error: {error_message}")
    
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
            
            # Process events to keep UI responsive
            QApplication.processEvents()
            
            # Check again if cancelled after processing events
            if self.is_cancelled:
                raise Exception("Download cancelled")
    
    def cancel(self):
        """Cancel the current download."""
        self.is_cancelled = True
