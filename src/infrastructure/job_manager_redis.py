import redis, os, json
from dataclasses import dataclass, field
from typing import Dict, Any
from utils.config import settings

REDIS_URL = settings.celery_broker_url
TEMP_DIR = settings.temp_dir

# redis-py expects host/port db, but can parse URL with from_url
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

@dataclass
class Job:
    job_id: str
    filename: str
    status: str = 'queued'
    result_path: str = None
    task_id: str = None
    _file_path: str = None

class JobManagerRedis:
    def __init__(self, temp_dir: str = None):
        self.temp_dir = TEMP_DIR
        os.makedirs(self.temp_dir, exist_ok=True)

    def create_job(self, filename: str) -> Job:
        import uuid
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        job = Job(job_id=job_id, filename=filename)
        # store minimal in redis
        redis_client.hset(f"job:{job_id}", mapping={"filename": filename, "status": job.status})
        return job

    def get_job(self, job_id: str) -> Dict[str, Any]:
        data = redis_client.hgetall(f"job:{job_id}")
        if not data:
            return None
        return data

    def save_file(self, job_id: str, content: bytes):
        path = os.path.join(self.temp_dir, f"{job_id}.pdf")
        with open(path, 'wb') as f:
            f.write(content)
        redis_client.hset(f"job:{job_id}", mapping={"_file_path": path})
        return path

    def set_job_field(self, job_id: str, key: str, value: str):
        redis_client.hset(f"job:{job_id}", key, value)

    def set_result(self, job_id: str, result: dict):
        # save json to file and store path
        path = os.path.join(self.temp_dir, f"{job_id}-result.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        redis_client.hset(f"job:{job_id}", mapping={"result_path": path, "status": "completed"})
