# Use the official Playwright image which includes all necessary system dependencies for Linux
FROM mcr.microsoft.com/playwright:v1.40.0-focal

# Label metadata
LABEL maintainer="kalidahmdev"
LABEL version="1.0.0"
LABEL description="Optimized Docker image for Cartoony Downloader"

# Set environment variables for Docker
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    DOWNLOAD_PATH=/app/downloads

# Set working directory
WORKDIR /app

# Copy configuration folder first for dependency installation (Better layer caching)
COPY config/requirements.txt ./config/

# Install Python dependencies as root
RUN pip3 install --no-cache-dir -r config/requirements.txt

# Copy the rest of the application code
COPY . .

# Create necessary directories and set permissions for the non-root user 'pwuser'
# 'pwuser' is UID 1000 in the playwright image
RUN mkdir -p downloads && \
    chown -R pwuser:pwuser /app

# Switch to the non-root user provided by the Playwright image
USER pwuser

# Expose the API port
EXPOSE 8000

# Run the FastAPI server
CMD ["python3", "src/api.py"]
