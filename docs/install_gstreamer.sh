#!/bin/bash

# GStreamer Installation Script for macOS
# This script installs GStreamer and its dependencies using Homebrew

set -e

echo "=========================================="
echo "GStreamer Installation Script for macOS"
echo "=========================================="

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Error: Homebrew is not installed."
    echo "Please install Homebrew first:"
    echo "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "Updating Homebrew..."
brew update

echo "Installing GStreamer core packages..."
brew install gstreamer

echo "Installing GStreamer plugins..."
# Good plugins (base, good, ugly, bad)
brew install gst-plugins-base
brew install gst-plugins-good
brew install gst-plugins-ugly
brew install gst-plugins-bad

echo "Installing Python GObject bindings..."
# This provides the python bindings for GStreamer
brew install pygobject3

echo "Installing GStreamer FFmpeg plugins..."
brew install gst-libav

echo "=========================================="
echo "Verifying installation..."
echo "=========================================="

# Verify core installation
if command -v gst-inspect-1.0 &> /dev/null; then
    echo "✓ GStreamer core installed successfully"
    gst-inspect-1.0 --version
else
    echo "✗ GStreamer core not found in PATH"
    exit 1
fi

# Verify plugins
echo ""
echo "Installed plugins:"
gst-inspect-1.0 -l | head -20

echo ""
echo "=========================================="
echo "Installation completed successfully!"
echo "=========================================="
echo ""
echo "To use GStreamer in Python, you may need to install PyGObject:"
echo "pip install PyGObject"
echo ""
echo "Note: On macOS, you might need to set the GST_PLUGIN_PATH:"
echo "export GST_PLUGIN_PATH=/usr/local/lib/gstreamer-1.0"
echo ""
echo "For video analysis, you typically need these additional packages:"
echo "brew install opencv"
echo "pip install opencv-python"
