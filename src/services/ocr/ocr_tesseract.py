from pdf2image import convert_from_path
import pytesseract, os
from typing import List, Dict
from services.ocr.iocr_service import IOcrService
from utils.config import settings

TESSERACT_CMD = settings.tess_cmd

if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

class OcrTesseract(IOcrService):
    def __init__(self, dpi: int = 300):
        self.dpi = dpi

    def ocr_pdf(self, pdf_path: str) -> List[Dict]:
        imgs = convert_from_path(pdf_path, dpi=self.dpi)
        pages = []
        for i, img in enumerate(imgs, start=1):
            text = pytesseract.image_to_string(img, lang="vie+eng")
            pages.append({"page": i, "text": text})
        return pages

    def _adjust_text(self, text: str) -> str:
        lines = text.splitlines()
        adjusted_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                adjusted_lines.append(stripped)
        return "\n".join(adjusted_lines)