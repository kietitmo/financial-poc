import json
import openai
from typing import Dict, Any, List
from domain.iai_client import IAIClient
from utils.config import settings

OPENAI_KEY = settings.openai_api_key

if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

class OpenAIClient(IAIClient):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model

    def detect_clusters(self, pages: List[Dict[str, Any]]) -> Dict[str, Any]:
        text_sample = "\n".join([f"Page {p['page']}: {p['text'][:500]}" for p in pages])
        prompt = (
            "Hãy đọc văn bản OCR từ báo cáo tài chính và xác định các phần chính "
            "(clusters: Bảng cân đối kế toán, KQKD, Lưu chuyển tiền tệ, Thuyết minh...). "
            "Trả về JSON với key 'clusters' là list object {cluster_id, title, start_page, end_page}.\n\n"
            + text_sample
        )
        if not OPENAI_KEY:
            return {"clusters": []}
        resp = openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        try:
            return json.loads(resp.choices[0].message["content"])
        except Exception:
            return {"clusters": []}
