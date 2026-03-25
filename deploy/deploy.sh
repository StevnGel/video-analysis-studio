#!/bin/bash

# Deployment script for video analysis studio

echo "Starting deployment..."

# Build the Docker image
echo "Building Docker image..."
docker build -t video-analysis-studio -f deploy/Dockerfile .

# Run the Docker container
echo "Running Docker container..."
docker run -d -p 8000:8000 --name video-analysis-studio video-analysis-studio

echo "Deployment completed successfully!"
echo "Application is running at http://localhost:8000"
