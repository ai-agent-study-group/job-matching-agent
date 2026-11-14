"""FastAPI 앱의 OpenAPI 스펙을 web/lib/api-types/openapi.json에 저장. 서버는 띄우지 않음."""

import json
from pathlib import Path

from main import app

OUT = Path(__file__).resolve().parents[1] / "web/lib/api-types/openapi.json"

OUT.write_text(json.dumps(app.openapi(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
