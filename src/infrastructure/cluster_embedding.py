from sentence_transformers import SentenceTransformer
import hdbscan
from typing import List
from domain.iclusterer import IClusterer

class EmbeddingClusterer(IClusterer):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def cluster(self, texts: List[str]):
        embs = self.model.encode(texts, convert_to_numpy=True)
        clusterer = hdbscan.HDBSCAN(min_cluster_size=2, metric="euclidean")
        labels = clusterer.fit_predict(embs)
        clusters = []
        mapping = {}
        for i, lbl in enumerate(labels):
            key = str(int(lbl)) if lbl >= 0 else "noise"
            mapping.setdefault(key, []).append(i+1)
        idx = 1
        for k, pages_list in mapping.items():
            clusters.append({
                "cluster_id": f"cluster_{idx}",
                "title": f"Cluster {k}",
                "start_page": min(pages_list),
                "end_page": max(pages_list),
                "page_count": len(pages_list)
            })
            idx += 1
        return clusters
