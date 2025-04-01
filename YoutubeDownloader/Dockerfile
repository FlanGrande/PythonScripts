FROM tobix/pywine:3.10

# Install required Python packages for both Windows and Linux
RUN wine pip install pyqt6 yt-dlp pyinstaller
RUN pip install pyqt6 yt-dlp pyinstaller

# Download and extract ffmpeg for Windows and install Linux ffmpeg
RUN apt-get update && apt-get install -y wget unzip ffmpeg && \
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

# Copy the PyInstaller spec files
COPY FlanYD-Win.spec FlanYD-Linux.spec /app/

# Create a build script
RUN echo '#!/bin/bash\n\
echo "Building Windows version..."\n\
wine pyinstaller FlanYD-Win.spec\n\
echo "Building Linux version..."\n\
pyinstaller FlanYD-Linux.spec\n\
echo "Build complete!"\n\
' > /app/build.sh && chmod +x /app/build.sh

# Build both Windows and Linux executables
CMD ["/app/build.sh"]
