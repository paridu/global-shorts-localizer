# Data Pipeline Specification: Media Ingestion & Extraction

## 1. Overview
This pipeline is the first point of contact for creator content. It is designed to handle diverse video formats and normalize them for the **GlobalVoice AI** inference engine.

## 2. Technical Decisions
- **yt-dlp**: Chosen over `pytube` for its superior maintenance record and support for a wider array of content platforms.
- **FFmpeg (via ffmpeg-python)**: The industry standard for media manipulation. We normalize audio to **16kHz Mono WAV** to ensure maximum compatibility and accuracy for the OpenAI Whisper v3 STT engine.
- **Task-ID Centricity**: Every ingestion generates a UUID4. This ID tracks the asset through translation, voice cloning, and final muxing.

## 3. Storage Strategy
- **Raw Storage (`/data/raw_videos`)**: Retained for 7 days (cache) or moved to Cold Storage (S3 Glacier) for long-term reference if the user selects a premium tier.
- **Processed Audio (`/data/extracted_audio`)**: Transient storage used for STT. Deleted once the transcript is verified.

## 4. Error Handling
- Retries are implemented at the Orchestrator level for network-related ingestion failures.
- FFmpeg stderr is captured and logged to identify corrupted video containers immediately.