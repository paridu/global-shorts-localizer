import logging
from src.ingestion.video_processor import VideoIngestionService
from src.ingestion.audio_extractor import AudioExtractionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ETL_Orchestrator")

class IngestionPipeline:
    """
    Orchestrates the flow from raw source to processed media assets.
    This serves as the entry point for the Data Engineering layer.
    """
    def __init__(self):
        self.ingestor = VideoIngestionService()
        self.extractor = AudioExtractionService()

    def run(self, source_url: str):
        try:
            # Step 1: Ingest Video
            logger.info("--- Phase 1: Ingestion ---")
            video_meta = self.ingestor.ingest_from_url(source_url)
            
            # Step 2: Extract Audio for AI Processing
            logger.info("--- Phase 2: Audio Extraction ---")
            audio_path = self.extractor.extract_audio(
                video_meta['file_path'], 
                video_meta['task_id']
            )
            
            # Finalize Status
            pipeline_result = {
                **video_meta,
                "audio_path": audio_path,
                "pipeline_status": "ready_for_ai_inference"
            }
            
            logger.info(f"Pipeline finished successfully for Task: {video_meta['task_id']}")
            return pipeline_result

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    # Sample Test Execution
    pipeline = IngestionPipeline()
    # Test with a short sample if running locally
    # pipeline.run("https://www.youtube.com/watch?v=example")