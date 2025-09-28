import json, re
from typing import Dict, Any, List
import google.generativeai as genai
from domain.iai_client import IAIClient
from utils.config import settings

GEMINI_KEY = settings.google_api_key

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

class GeminiClient(IAIClient):
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model

    def detect_clusters(self, pages: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not GEMINI_KEY:
            return {"clusters": []}

        text_sample = "\n".join(
            [f"Page {p['page']}: {p['text'][:500]}" for p in pages]
        )
        prompt = (
            "Hãy đọc văn bản OCR từ báo cáo tài chính và xác định các phần chính "
            "(clusters: Bảng cân đối kế toán, KQKD, Lưu chuyển tiền tệ, Thuyết minh...). "
            "Trả về JSON với key 'clusters' là list object {cluster_id, title, start_page, end_page}.\n\n"
            + text_sample
        )

        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            text = response.text or "{}"
            cleaned = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
            return json.loads(cleaned)
        except Exception as e:
            return {"clusters": []}
