from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from infrastructure.job_manager_redis import JobManagerRedis
from application.tasks import process_pdf_task
import os

router = APIRouter()
job_mgr = JobManagerRedis()

@router.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF supported")
    job = job_mgr.create_job(file.filename)
    data = await file.read()
    file_path = job_mgr.save_file(job.job_id, data)

    async_result = process_pdf_task.delay(file_path, job.job_id)
    job_mgr.set_job_field(job.job_id, "task_id", async_result.id)
    job_mgr.set_job_field(job.job_id, "status", "queued")
    return JSONResponse({"success": True, "job_id": job.job_id, "task_id": async_result.id})

@router.get("/status/{job_id}")
def get_status(job_id: str):
    job = job_mgr.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job

@router.get("/download/{job_id}")
def download_result(job_id: str):
    job = job_mgr.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    result_path = job.get("result_path")
    if not result_path or not os.path.exists(result_path):
        raise HTTPException(status_code=404, detail="result not ready")
    return FileResponse(result_path, media_type="application/json", filename=f"{job_id}-result.json")
