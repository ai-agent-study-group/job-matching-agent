"""JobServicePort (get_usage · search_jobs · get_job)."""

from abc import ABC, abstractmethod
from typing import Any

from domain.job import JobPosting


class JobServicePort(ABC):
    """MCP 서버 · JMA 앱에 제공하는 기능 목록."""

    @abstractmethod
    async def get_usage(self) -> dict[str, Any]:
        """JSON schema of the search_jobs parameters."""

    @abstractmethod
    async def search_jobs(self, params: dict[str, Any]) -> list[JobPosting]:
        """Search job postings."""

    @abstractmethod
    async def get_job(self, posting_id: str) -> JobPosting:
        """Return one posting with its description."""
