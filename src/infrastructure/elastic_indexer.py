from elasticsearch import Elasticsearch
from domain.iindexer import IIndexer
from utils.config import settings

ES_URL = settings.elastic_url

class ElasticIndexer(IIndexer):
    def __init__(self):
        self.es = Elasticsearch(ES_URL)

    def index_job(self, job_id: str, payload: dict):
        idx = 'bctc_jobs'
        if not self.es.indices.exists(index=idx):
            self.es.indices.create(index=idx)
        self.es.index(index=idx, id=job_id, document=payload)
