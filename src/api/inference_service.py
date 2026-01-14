from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import uuid
import os
from .engine.tts_cloner import MultiLingualVoiceEngine

app = FastAPI(title="GlobalVoice AI Inference API")

# Initialize Engine (Singleton for memory efficiency)
engine = MultiLingualVoiceEngine()

TEMP_UPLOAD_DIR = "uploads/temp"
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

@app.post("/v1/dub/generate")
async def generate_dub(
    text: str = Form(...),
    target_lang: str = Form(...),
    voice_sample: UploadFile = File(...)
):
    """
    Endpoint to receive a text string and a voice sample, 
    returning a cloned voice audio file.
    """
    session_id = str(uuid.uuid4())
    ref_path = os.path.join(TEMP_UPLOAD_DIR, f"{session_id}_ref.wav")
    
    # Save incoming reference sample
    try:
        with open(ref_path, "wb") as buffer:
            shutil.copyfileobj(voice_sample.file, buffer)
            
        # Run Inference
        output_file = f"{session_id}_output.wav"
        result_path = engine.generate_cloned_speech(
            text=text,
            language_code=target_lang,
            reference_audio_path=ref_path,
            output_filename=output_file
        )
        
        return FileResponse(result_path, media_type="audio/wav", filename=output_file)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup reference file to save disk space
        if os.path.exists(ref_path):
            os.remove(ref_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)