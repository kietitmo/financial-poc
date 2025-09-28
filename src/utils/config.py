import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str | None = None
    google_api_key: str = os.getenv('GEMINI_KEY', 'AIzaSyCYVKlKJZOtqvyjf0ATVwAWyuv6CU9amfE')

    elastic_url: str = os.getenv('ELASTIC_URL', 'http://localhost:9200')
    tess_cmd: str = os.getenv('TESSERACT_CMD', '')
    temp_dir: str = os.getenv('TEMP_DIR', './tmp')
    
    # celery
    celery_broker_url: str = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
    celery_result_backend: str = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/1')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
