# Database Architecture Documentation: GlobalVoice AI

## 1. Design Philosophy
The schema is designed to support a **Highly Asynchronous Media Pipeline**. Because AI dubbing involves multiple stages (Extraction -> Transcription -> Translation -> Voice Cloning -> TTS -> Lip-Sync), the database acts as the state machine for the entire process.

## 2. Entity Relationships
- **Users to Projects (1:N):** A user can manage multiple localization projects.
- **Projects to Media Assets (1:N):** Each project tracks multiple files, including the source video, the intermediate audio stems, and final localized renders.
- **Projects to Workflow Tasks (1:N):** This is the heart of the "Micro-Service Orchestration." Every AI action is logged as a task to allow for retries, cost tracking (GPU minutes), and status reporting to the frontend.
- **Languages & Voices:** A global lookup for supported locales and the specific voice models (cloned or synthetic) used during the TTS phase.

## 3. Data Integrity & Scalability
- **JSONB for Transcripts:** We use `JSONB` for transcripts and translations. This allows for flexible storage of timestamps, speaker diarization data, and word-level confidence scores without requiring complex join tables for every word.
- **UUIDs:** All primary keys use UUIDs to prevent ID enumeration and to facilitate future database sharding across regions.
- **Audit Trails:** `created_at` and `updated_at` are enforced on all critical tables to monitor system latency and AI processing bottlenecks.

## 4. Operational Considerations
- **Storage:** The `media_assets` table does not store binary data; it stores **S3 URIs**. The application logic (FastAPI) handles pre-signed URLs for secure access.
- **Queueing:** The `workflow_tasks` table is designed to be polled by or integrated with a worker system (like Celery or Temporal) to ensure no video processing job is lost during pod restarts.