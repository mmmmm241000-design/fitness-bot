# FitCoach Bot - Dockerfile for Render
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY bot/ ./bot/
COPY config/ ./config/
COPY data/ ./data/
RUN mkdir -p logs

# Create necessary directories
RUN mkdir -p data logs config

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATABASE_PATH=data/fitness.db
ENV LOG_LEVEL=INFO

# Expose port (for health checks)
EXPOSE 8000

# Run the bot
CMD ["python", "bot/main.py"]
