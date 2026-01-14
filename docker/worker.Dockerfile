# GlobalVoice AI: Worker Node Container
# Optimized for GPU-accelerated AI Inference

FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Link python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy requirements and install
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download models (Optimization for fast startup)
RUN python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"

# Copy source code
COPY src/ /app/src/

# Command to run the worker
CMD ["celery", "-A", "src.worker.tasks", "worker", "--loglevel=info", "-Q", "ai_tasks", "-c", "1"]