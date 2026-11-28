import json
from pathlib import Path

from main import app

SPEC = Path(__file__).parents[4] / "web/lib/api-types/openapi.json"


def test_committed_openapi_spec_matches_the_app():
    # 다르면 web/에서: npm run generate:types
    assert json.loads(SPEC.read_text(encoding="utf-8")) == app.openapi()


def test_profile_422_lists_both_detail_shapes():
    """/api/profile의 422는 detail 배열(폼 검증)과 문장(파일) 두 형식을 다 적는다.

    목적: 생성된 TS 타입에 배열만 있으면 FE가 문장 detail을 놓침. 직접 적은 $ref가 실제 스키마를 가리키는지도 확인.
    """
    spec = app.openapi()
    response = spec["paths"]["/api/profile"]["post"]["responses"]["422"]
    schema = response["content"]["application/json"]["schema"]
    names = [ref["$ref"].rsplit("/", 1)[-1] for ref in schema["anyOf"]]

    assert names == ["HTTPValidationError", "ErrorDTO"]
    assert set(names) <= spec["components"]["schemas"].keys()
