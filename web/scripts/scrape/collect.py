"""지정한 공식 페이지를 가져와 검토 대기 JSON에 저장합니다."""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_HOSTS = {"weworkremotely.com", "www.linkedin.com"}

def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)

def validate_spec(spec):
    import re
    if not re.fullmatch(r"[a-z0-9-]+", spec["id"]) or spec["domain"] not in {"backend", "data"}:
        raise ValueError("공고 ID 또는 분야가 잘못되었습니다.")
    url = urlparse(spec["url"])
    if url.scheme != "https" or url.hostname not in ALLOWED_HOSTS:
        raise ValueError("허용한 채용 사이트의 HTTPS 주소만 수집할 수 있습니다.")

def fetch_html(url):
    request = Request(url, headers={"User-Agent": "ResumeMatchAgentStudy/0.1 (manual educational collection)"})
    with urlopen(request, timeout=20) as response:
        if urlparse(response.url).hostname not in ALLOWED_HOSTS:
            raise ValueError("허용하지 않은 주소로 이동했습니다.")
        if "html" not in response.headers.get("Content-Type", ""):
            raise ValueError("HTML 페이지가 아닙니다.")
        raw = response.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("자료가 너무 큽니다.")
        charset = response.headers.get_content_charset()
        return raw.decode(charset) if charset else raw

def extract_body(html, selector):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    if "Radware" in title or "Verifying your browser" in soup.get_text(" ", strip=True):
        raise ValueError("사이트가 자동 수집을 차단했습니다. 우회하지 않고 기존 검토 자료를 사용합니다.")
    for node in soup.select("script, style, nav, footer, header, dialog"):
        node.decompose()
    blocks = soup.select(selector)
    if not blocks:
        raise ValueError("본문 위치를 찾지 못했습니다. selector를 확인해주세요.")
    body = "\n".join(node.get_text(" ", strip=True) for node in blocks)
    if len(body) < 40:
        raise ValueError("추출한 본문이 너무 짧습니다.")
    return body[:40000]

def collect(specs, output_dir, fetcher=fetch_html):
    failures = 0
    for spec in specs:
        try:
            validate_spec(spec)
            body = extract_body(fetcher(spec["url"]), spec["selector"])
            result = {key: spec[key] for key in ("id", "domain", "title", "url", "keywords", "language")}
            result.update(body=body, collectedAt=datetime.now(timezone.utc).isoformat(), reviewed=False, reviewedAt="", kind="scraped")
            atomic_json(output_dir / (spec["id"] + ".json"), result)
            print("검토 대기 저장:", spec["id"])
        except Exception as error:
            failures += 1
            print("수집 실패:", spec.get("id", "unknown"), str(error), file=sys.stderr)
        time.sleep(0.3)
    return failures

def main():
    parser = argparse.ArgumentParser(description="공식 자료를 검토 대기 파일로 수집합니다. 앱 자료는 변경하지 않습니다.")
    parser.add_argument("--manifest", type=Path, default=ROOT / "scripts/scrape/sources.json")
    parser.add_argument("--output", type=Path, default=ROOT / "data/pending")
    args = parser.parse_args()
    if args.output.resolve() == (ROOT / "data").resolve():
        parser.error("앱 자료 폴더 대신 별도 검토 대기 폴더를 사용해주세요.")
    specs = json.loads(args.manifest.read_text(encoding="utf-8"))
    return 1 if collect(specs, args.output) else 0

if __name__ == "__main__":
    raise SystemExit(main())
