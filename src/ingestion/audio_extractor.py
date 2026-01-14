import ffmpeg
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AudioExtraction")

class AudioExtractionService:
    """
    ETL Component: Extracts high-quality audio from video containers
    standardizing the sample rate and format for downstream AI STT processing.
    """
    def __init__(self, output_path: str = "data/extracted_audio"):
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def extract_audio(self, video_path: str, task_id: str) -> str:
        """
        Uses FFmpeg to isolate audio. 
        Target: Mono, 16kHz, WAV (Optimal for Whisper/STT models).
        """
        target_file = self.output_path / f"{task_id}.wav"
        
        logger.info(f"Extracting audio from {video_path}...")
        
        try:
            (
                ffmpeg
                .input(video_path)
                .output(
                    str(target_file),
                    acodec='pcm_s16le',
                    ac=1,
                    ar='16k'
                )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            logger.info(f"Audio extraction complete: {target_file}")
            return str(target_file)
        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error: {e.stderr.decode()}")
            raise Exception("Failed to extract audio.") from e