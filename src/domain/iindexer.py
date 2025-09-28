from abc import ABC, abstractmethod

class IIndexer(ABC):
    @abstractmethod
    def index_job(self, job_id: str, payload: dict):
        pass
