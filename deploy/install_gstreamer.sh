#!/bin/bash

# Script to install GStreamer dependencies locally

echo "Installing GStreamer dependencies..."

# For macOS
if [[ "$(uname)" == "Darwin" ]]; then
    echo "Installing on macOS..."
    brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
    
elif [[ "$(uname)" == "Linux" ]]; then
    echo "Installing on Linux..."
    # For Ubuntu/Debian
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav
    # For CentOS/RHEL
    elif command -v yum &> /dev/null; then
        sudo yum install -y gstreamer1 gstreamer1-plugins-base gstreamer1-plugins-good gstreamer1-plugins-bad-free gstreamer1-plugins-ugly-free
    else
        echo "Unsupported Linux distribution"
        exit 1
    fi
else
    echo "Unsupported operating system"
    exit 1
fi

echo "GStreamer dependencies installed successfully!"
