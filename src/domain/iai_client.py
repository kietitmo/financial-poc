from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IAIClient(ABC):
    @abstractmethod
    def detect_clusters(self, pages: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass
