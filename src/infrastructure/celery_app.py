from celery import Celery

from utils.config import settings

CELERY_BROKER_URL = settings.celery_broker_url
CELERY_RESULT_BACKEND = settings.celery_result_backend

celery = Celery(
    "financial-poc",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["application.tasks"]
)
