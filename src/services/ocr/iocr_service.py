from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IOcrService(ABC):
    @abstractmethod
    def ocr_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        pass
