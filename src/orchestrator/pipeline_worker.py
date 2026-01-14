"""
GlobalVoice AI - Core Pipeline Orchestrator
Handles the sequence of AI inference tasks with error handling and state persistence.
"""

import asyncio
import logging
from typing import Dict, Any
from core.media_processor import MediaProcessor
from ai_modules.stt_engine import Transcriber
from ai_modules.translator import ContextualTranslator
from ai_modules.tts_engine import VoiceSynthesizer
from ai_modules.lipsync_engine import LipSyncProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PipelineWorker")

class DubbingOrchestrator:
    def __init__(self, job_config: Dict[str, Any]):
        self.job_id = job_config['job_id']
        self.input_path = job_config['input_path']
        self.target_langs = job_config['target_langs']
        self.voice_id = job_config.get('voice_id')
        
        # Initialize modules
        self.processor = MediaProcessor()
        self.stt = Transcriber(model_size="large-v3")
        self.nmt = ContextualTranslator()
        self.tts = VoiceSynthesizer()
        self.visuals = LipSyncProcessor()

    async def execute_workflow(self):
        try:
            logger.info(f"Starting Job {self.job_id}: Processing {self.input_path}")
            
            # 1. Extraction
            audio_path, video_path = await self.processor.extract_tracks(self.input_path)
            
            # 2. Transcription (STT)
            segments = await self.stt.transcribe(audio_path)
            logger.info(f"Transcription complete for {self.job_id}")

            results = []
            for lang in self.target_langs:
                # 3. Translation
                translated_segments = await self.nmt.translate_batch(segments, target_lang=lang)
                
                # 4. Voice Synthesis (TTS)
                dubbed_audio = await self.tts.generate_cloned_speech(
                    translated_segments, 
                    voice_id=self.voice_id,
                    reference_audio=audio_path
                )
                
                # 5. Lip-Sync (The most heavy task - can be toggled)
                final_video = await self.visuals.sync_video(
                    video_path, 
                    dubbed_audio, 
                    quality_mode="high-res"
                )
                
                output_path = f"exports/{self.job_id}_{lang}.mp4"
                await self.processor.finalize(final_video, output_path)
                results.append({"lang": lang, "url": output_path})

            logger.info(f"Job {self.job_id} successfully completed.")
            return {"status": "success", "outputs": results}

        except Exception as e:
            logger.error(f"Job {self.job_id} failed: {str(e)}")
            # Trigger cleanup and notification service
            return {"status": "failed", "error": str(e)}

# Example Usage (Integration with Task Queue)
# orchestrator = DubbingOrchestrator(job_data)
# asyncio.run(orchestrator.execute_workflow())