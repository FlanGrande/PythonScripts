#!/bin/bash
# Build script for creating a maximally portable Linux executable

echo "Building static Linux executable..."

# Build using Docker with older glibc for compatibility
docker run -v "$(pwd):/host" -e PYTHONOPTIMIZE=2 flanyd-linux sh -c "
cd /app

# Clean previous builds
rm -rf build dist

# Build with PyInstaller using aggressive optimization
pyinstaller --onefile \
    --windowed \
    --add-binary '/app/ffmpeg/ffmpeg:.' \
    --add-binary '/app/ffmpeg/ffprobe:.' \
    --add-data 'FlanYDLogo.png:.' \
    --add-data 'FlanYDLogo.ico:.' \
    --icon=FlanYDLogo.png \
    --name FlanYD \
    --strip \
    --optimize 2 \
    youtube_downloader_ui.py

# Copy the result
cp dist/FlanYD /host/dist/FlanYD-linux-static
"

echo "Build complete! Checking the executable..."
file dist/FlanYD-linux-static
ldd dist/FlanYD-linux-static 2>/dev/null | head -10 || echo "No dynamic dependencies found (good for static build)"
ls -lah dist/FlanYD-linux-static