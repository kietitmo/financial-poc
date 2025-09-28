Financial Report OCR + Clustering (SOLID + Celery + Logger + Settings)
======================================================================

Features:
- FastAPI app (upload, check status, download results)
- Celery worker (async OCR + clustering pipeline)
- Redis (broker + state)
- Elasticsearch (indexing)
- Logger (structured logs with job_id)
- Pydantic Settings (centralized config, loads from .env)

Usage:
1. Copy `.env.example` to `.env` and set your OPENAI_API_KEY.
2. Run: `docker-compose up --build`
3. Upload PDF: POST /api/pdf/process
4. Check status: GET /api/pdf/status/{job_id}
5. Download result: GET /api/pdf/download/{job_id}
