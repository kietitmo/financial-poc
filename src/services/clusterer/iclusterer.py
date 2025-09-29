from abc import ABC, abstractmethod
from typing import List, Any

class IClusterer(ABC):
    @abstractmethod
    def cluster(self, texts: List[str]) -> Any:
        pass
