import uuid
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Internal imports (Refencing established architecture)
from src.worker.tasks import process_video_workflow
from src.worker.celery_app import celery_app

app = FastAPI(
    title="GlobalVoice AI API",
    description="Backend orchestration for AI-driven video dubbing and localization.",
    version="1.0.0"
)

# --- Models ---

class DubbingRequest(BaseModel):
    video_url: Optional[str] = None
    file_id: Optional[str] = None
    target_languages: List[str]
    voice_cloning: bool = True
    priority: int = 1

class JobStatusResponse(BaseModel):
    job_id: str
    project_id: str
    status: str
    progress: float
    created_at: datetime
    updated_at: datetime

# --- Endpoints ---

@app.post("/jobs/dub", response_model=JobStatusResponse, status_code=202)
async def create_dubbing_job(request: DubbingRequest):
    """
    Initializes a dubbing project. Triggers the asynchronous processing pipeline.
    """
    if not request.video_url and not request.file_id:
        raise HTTPException(status_code=400, detail="Either video_url or file_id must be provided.")
    
    project_id = str(uuid.uuid4())
    
    # Trigger Celery Task Chain
    # The chain handles: Ingestion -> STT -> Translation -> TTS -> Final Assembly
    task = process_video_workflow.delay(
        project_id=project_id,
        video_source=request.video_url or request.file_id,
        target_langs=request.target_languages,
        cloning_enabled=request.voice_cloning
    )
    
    return {
        "job_id": task.id,
        "project_id": project_id,
        "status": "PENDING",
        "progress": 0.0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@app.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Polls the status of a specific background job.
    """
    task_result = celery_app.AsyncResult(job_id)
    
    # Map Celery states to our API states
    status_mapping = {
        "PENDING": "queued",
        "STARTED": "processing",
        "SUCCESS": "completed",
        "FAILURE": "failed",
        "RETRY": "retrying"
    }
    
    # In a production scenario, we would also query the DB for detailed metadata
    # as defined in database/schema.sql
    
    return {
        "job_id": job_id,
        "project_id": "ext-ref-id", # Placeholder for DB lookup
        "status": status_mapping.get(task_result.state, "unknown"),
        "progress": 1.0 if task_result.state == "SUCCESS" else 0.5, # Simplified
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@app.delete("/jobs/{job_id}")
async def cancel_job(job_id: str):
    """
    Terminates a running job and cleans up temporary resources.
    """
    celery_app.control.revoke(job_id, terminate=True)
    return {"message": f"Job {job_id} revocation signal sent."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)