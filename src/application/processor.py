from domain.iocr_service import IOcrService
from domain.iai_client import IAIClient
from domain.iclusterer import IClusterer
from domain.iindexer import IIndexer
from utils.logger import get_logger

logger = get_logger(__name__)

class Processor:
    def __init__(self, ocr: IOcrService, ai: IAIClient,
                 clusterer: IClusterer, indexer: IIndexer):
        self.ocr = ocr
        self.ai = ai
        self.clusterer = clusterer
        self.indexer = indexer

    def process_pdf(self, pdf_path: str, job_id: str):
        logger.info(f"[{job_id}] OCR started")
        pages = self.ocr.ocr_pdf(pdf_path)
        logger.info(f"[{job_id}] OCR done, {len(pages)} pages")

        logger.info(f"[{job_id}] Detecting clusters with AI")
        clusters_ai = self.ai.detect_clusters(pages[:30])
        logger.debug(f"[{job_id}] AI clusters: {clusters_ai}")
        if clusters_ai.get("clusters"):
            logger.info(f"[{job_id}] AI detected {len(clusters_ai['clusters'])} clusters")
        else:
            logger.info(f"[{job_id}] AI did not detect clusters, fallback to ML")
        
        # logger.info(f"[{job_id}] Semantic clustering with embeddings")
        # texts = [p.get("text", "") for p in pages]
        # clusters_ml = self.clusterer.cluster(texts)

        layout = {"clusters": clusters_ai.get("clusters", [])}
        self.indexer.index_job(job_id, {"layout": layout, "meta": {"pages": len(pages)}})
        logger.info(f"[{job_id}] Indexed into Elasticsearch")
        return layout
