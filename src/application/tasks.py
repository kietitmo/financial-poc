from infrastructure.celery_app import celery
from application.processor import Processor
from infrastructure.ocr_tesseract import OcrTesseract
from infrastructure.ai_openai import OpenAIClient
from infrastructure.ai_gemini import GeminiClient
from infrastructure.cluster_embedding import EmbeddingClusterer
from infrastructure.elastic_indexer import ElasticIndexer
from infrastructure.job_manager_redis import JobManagerRedis
from utils.logger import get_logger

logger = get_logger(__name__)

@celery.task(bind=True)
def process_pdf_task(self, pdf_path: str, job_id: str):
    logger.info(f"[{job_id}] Task started")
    job_mgr = JobManagerRedis()
    processor = Processor(
        ocr=OcrTesseract(),
        ai=GeminiClient(),
        clusterer=EmbeddingClusterer(),
        indexer=ElasticIndexer(),
    )
    try:
        layout = processor.process_pdf(pdf_path, job_id)
        result = {"layout": layout, "job_id": job_id}
        job_mgr.set_result(job_id, result)
        logger.info(f"[{job_id}] Completed successfully")
        return {"status": "ok", "job_id": job_id}
    except Exception as e:
        job_mgr.set_job_field(job_id, "status", "failed")
        job_mgr.set_job_field(job_id, "error", str(e))
        logger.exception(f"[{job_id}] Failed")
        return {"status": "error", "error": str(e)}
