import sys
from yt_dlp import YoutubeDL

def download_youtube_video(url):
    try:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_video.py <YouTube_URL>")
    else:
        download_youtube_video(sys.argv[1])


