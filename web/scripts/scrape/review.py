"""사람이 원문과 내용을 확인한 뒤 명시적으로 승인할 때만 앱 자료에 반영합니다."""
import argparse
import json
import re
from datetime import UTC, datetime

from collect import ROOT, atomic_json, validate_spec


def approve(source_id, data_dir=ROOT / "data"):
    if not re.fullmatch(r"[a-z0-9-]+", source_id):
        raise ValueError("올바른 자료 ID를 입력해주세요.")
    candidate = json.loads((data_dir / "pending" / (source_id + ".json")).read_text(encoding="utf-8"))
    validate_spec(candidate)
    if candidate["id"] != source_id or not isinstance(candidate.get("body"), str) or len(candidate["body"]) < 40:
        raise ValueError("자료 ID와 본문을 확인해주세요.")
    if not isinstance(candidate.get("keywords"), list) or not all(isinstance(k, str) for k in candidate["keywords"]):
        raise ValueError("검색 키워드를 확인해주세요.")
    if candidate.get("kind") != "scraped" or not candidate.get("language") or not candidate.get("collectedAt"):
        raise ValueError("수집 메타데이터를 확인해주세요.")
    path = data_dir / (candidate["domain"] + ".json")
    current = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    candidate.update(reviewed=True, reviewedAt=datetime.now(UTC).isoformat())
    atomic_json(path, [s for s in current if s["id"] != source_id] + [candidate])
    print("검토 승인 반영:", source_id)

def main():
    parser = argparse.ArgumentParser(description="원문과 비교하고 개인정보·불필요한 내용을 제거한 자료를 승인합니다.")
    parser.add_argument("--approve", required=True, help="직접 검토를 마친 자료 ID")
    args = parser.parse_args()
    approve(args.approve)

if __name__ == "__main__":
    main()
