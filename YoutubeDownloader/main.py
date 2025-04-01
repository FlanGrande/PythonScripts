import sys
from yt_dlp import YoutubeDL

def download_youtube_video(url):
    try:
        ydl_opts = {
            'format': 'bestvideo[height<=1081]+bestaudio/best[height<=1080]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download completed for: {url}")
    except Exception as e:
        print(f"An error occurred for {url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_video.py <YouTube_URL1> [<YouTube_URL2> ...]")
        sys.exit(1)
    
    # Skip the first argument (script name) and process all URLs
    urls = sys.argv[1:]
    for url in urls:
        download_youtube_video(url)