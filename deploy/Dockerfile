# Use ultralytics image as base
FROM ultralytics/ultralytics:latest

# Set working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install additional dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install GStreamer dependencies
RUN apt-get update && apt-get install -y \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    && rm -rf /var/lib/apt/lists/*

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "backend/main.py"]
