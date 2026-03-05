# Use the official Playwright image which includes all necessary system dependencies for Linux
FROM mcr.microsoft.com/playwright:v1.40.0-focal

# Set working directory
WORKDIR /app

# Copy configuration folder first for dependency installation
COPY config/requirements.txt ./config/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r config/requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the downloads directory exists
RUN mkdir -p downloads

# Set environment variables for Docker
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV DOWNLOAD_PATH=/app/downloads
ENV HEADLESS=True

# Expose the API port
EXPOSE 8000

# Run the FastAPI server
CMD ["python3", "src/api.py"]
