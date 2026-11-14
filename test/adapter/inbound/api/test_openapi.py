import json
from pathlib import Path

from main import app

SPEC = Path(__file__).parents[4] / "web/lib/api-types/openapi.json"


def test_committed_openapi_spec_matches_the_app():
    # 다르면 web/에서: npm run generate:types
    assert json.loads(SPEC.read_text(encoding="utf-8")) == app.openapi()
