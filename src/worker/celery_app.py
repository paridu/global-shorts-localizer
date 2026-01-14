import os
from celery import Celery

# Configuration for Redis as the Message Broker and Result Backend
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "globalvoice_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.worker.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600, # 1 hour max for video processing
    worker_prefetch_multiplier=1 # Ensure fair distribution for heavy tasks
)