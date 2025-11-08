#!/bin/bash

# Build script for creating FlanYD Flatpak

echo "Building FlanYD Flatpak..."

# 1. Install the required runtime and SDK
flatpak install --user flathub org.freedesktop.Platform//23.08 org.freedesktop.Sdk//23.08

# 2. Build the Flatpak
flatpak-builder --force-clean --user --install-deps-from=flathub --repo=repo --install builddir io.github.flanyd.FlanYD.yml

# 3. Test run the application
echo "Testing the Flatpak build..."
flatpak run io.github.flanyd.FlanYD

# 4. Create a single-file bundle for distribution
flatpak build-bundle repo FlanYD.flatpak io.github.flanyd.FlanYD --runtime-repo=https://flathub.org/repo/flathub.flatpakrepo

echo "Flatpak bundle created: FlanYD.flatpak"
echo "Users can install it with: flatpak install --user FlanYD.flatpak"