FROM tobix/pywine:3.10

# Install required Python packages
RUN wine pip install pyqt6 yt-dlp pyinstaller

# Download and extract ffmpeg for Windows
RUN apt-get update && apt-get install -y wget unzip && \
    wget -q https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip -O /tmp/ffmpeg.zip && \
    unzip -q /tmp/ffmpeg.zip -d /tmp && \
    mkdir -p /app/ffmpeg && \
    cp /tmp/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe /app/ffmpeg/ && \
    cp /tmp/ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe /app/ffmpeg/ && \
    rm -rf /tmp/ffmpeg.zip /tmp/ffmpeg-master-latest-win64-gpl

# Set up working directory
WORKDIR /app

# Copy application files
COPY main.py downloader.py youtube_downloader_ui.py /app/

# Copy the branding assets
COPY FlanYDLogo.ico FlanYDLogo.png /app/

# Copy the PyInstaller spec file
COPY FlanYD.spec /app/

# Build the executable using the spec file
CMD wine pyinstaller FlanYD.spec
