import os
import torch
import torchaudio
from TTS.api import TTS
from typing import List, Optional

class MultiLingualVoiceEngine:
    """
    Core Voice Engine for GlobalVoice AI.
    Utilizes XTTS v2 for high-fidelity multi-lingual voice cloning and neural TTS.
    Supports 16+ languages including Thai, English, Spanish, and Japanese.
    """
    def __init__(self, model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[INFO] Initializing Voice Engine on {self.device}...")
        
        # Initialize the TTS model
        self.tts = TTS(model_name).to(self.device)
        self.output_dir = "outputs/cloned_audio"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_cloned_speech(
        self, 
        text: str, 
        language_code: str, 
        reference_audio_path: str, 
        output_filename: str
    ) -> str:
        """
        Generates speech using a reference audio file for voice cloning.
        
        Args:
            text: The localized text to be spoken.
            language_code: Target language (e.g., 'th', 'en', 'es').
            reference_audio_path: Path to the 6-10 second source voice sample.
            output_filename: Name of the resulting .wav file.
        """
        output_path = os.path.join(self.output_dir, output_filename)
        
        print(f"[PROCESS] Synthesizing speech for language: {language_code}...")
        
        # Generate speech
        self.tts.tts_to_file(
            text=text,
            speaker_wav=reference_audio_path,
            language=language_code,
            file_path=output_path
        )
        
        return output_path

    def list_supported_languages(self) -> List[str]:
        return self.tts.languages

if __name__ == "__main__":
    # Example Usage: Cloning a Thai voice for a global creator
    engine = MultiLingualVoiceEngine()
    
    # Example parameters
    sample_text = "สวัสดีครับ ยินดีต้อนรับสู่แพลตฟอร์มสร้างสรรค์คอนเทนต์ระดับโลก"
    ref_voice = "data/samples/creator_voice_sample.wav" # 6s sample of the user
    
    output = engine.generate_cloned_speech(
        text=sample_text,
        language_code="th",
        reference_audio_path=ref_voice,
        output_filename="thai_dub_v1.wav"
    )
    print(f"[SUCCESS] Audio generated at: {output}")