"""PoC: Greenhouse 공개 Job Board API를 MCP 도구로 노출하는 stdio 서버.

실행: uv run --group poc poc/mcp_server.py
"""

import html
import re

import httpx2
from fastmcp import FastMCP

GREENHOUSE = "https://boards-api.greenhouse.io/v1/boards"

mcp = FastMCP("jobs")


@mcp.tool
def list_jobs(board: str, keyword: str = "") -> list[dict]:
    """Greenhouse 보드의 공고 목록 (id, 제목, 위치).

    board: 회사 board token. 공고 URL job-boards.greenhouse.io/<board>/jobs/... 의 <board>.
    keyword: 제목 부분 일치 필터 (대소문자 무시). 보드에 공고가 수백 개일 수 있으니 가능하면 지정.
    결과가 비면 더 짧거나 다른 키워드로 다시 시도.
    """
    jobs = httpx2.get(f"{GREENHOUSE}/{board}/jobs").raise_for_status().json()["jobs"]
    return [
        {"id": j["id"], "title": j["title"], "location": j["location"]["name"]}
        for j in jobs
        if keyword.lower() in j["title"].lower()
    ]


@mcp.tool
def get_job(board: str, job_id: int) -> str:
    """공고 하나의 제목, 위치, 본문을 텍스트로 반환."""
    job = httpx2.get(f"{GREENHOUSE}/{board}/jobs/{job_id}").raise_for_status().json()
    return f"# {job['title']}\n{job['location']['name']}\n\n{_html_to_text(job['content'])}"


def _html_to_text(content: str) -> str:
    # content는 HTML이 한 번 이스케이프된 문자열이라 먼저 풀어야 태그가 보임
    text = html.unescape(content)
    text = re.sub(r"<li[^>]*>", "- ", text)
    text = re.sub(r"<br\s*/?>|</(p|div|li|h\d|ul|ol)>", "\n", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


if __name__ == "__main__":
    mcp.run()
