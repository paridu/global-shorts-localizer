import os
import uuid
import logging
from pathlib import Path
import yt_dlp
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VideoIngestion")

class VideoIngestionService:
    """
    Handles the initial ingestion of video content from various sources.
    Supports local uploads and URL-based ingestion (YouTube, etc.)
    """
    def __init__(self, download_path: str = "data/raw_videos"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(parents=True, exist_ok=True)

    def ingest_from_url(self, url: str) -> Dict[str, Any]:
        """
        Downloads video using yt-dlp and extracts initial metadata.
        """
        task_id = str(uuid.uuid4())
        output_template = str(self.download_path / f"{task_id}.%(ext)s")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'quiet': True,
            'noplaylist': True,
        }

        logger.info(f"Starting ingestion for URL: {url} | Task ID: {task_id}")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                metadata = {
                    "task_id": task_id,
                    "original_url": url,
                    "title": info.get("title"),
                    "duration": info.get("duration"),
                    "ext": info.get("ext"),
                    "file_path": file_path,
                    "status": "ingested"
                }
                logger.info(f"Successfully ingested: {metadata['title']}")
                return metadata
        except Exception as e:
            logger.error(f"Failed to ingest URL {url}: {str(e)}")
            raise

    def process_local_upload(self, temp_path: str) -> Dict[str, Any]:
        """
        Moves a locally uploaded file to the managed storage area.
        """
        task_id = str(uuid.uuid4())
        file_ext = Path(temp_path).suffix
        target_path = self.download_path / f"{task_id}{file_ext}"
        
        os.rename(temp_path, target_path)
        
        return {
            "task_id": task_id,
            "file_path": str(target_path),
            "status": "ingested"
        }