"""Source outbound 포트 (Source 관련 어댑터와 호환)"""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from domain.job import JobPosting


class JobSource(ABC):
    """공고 출처 outbound 포트. 어댑터의 source 부분에서 구현."""

    @abstractmethod
    async def usage(self) -> type[BaseModel]:
        """The DTO class of this source's search parameters."""

    @abstractmethod
    async def search(self, params: dict[str, Any]) -> list[JobPosting]:
        """Validate params against the usage DTO and return matching postings."""

    @abstractmethod
    async def fetch(self, posting_id: str) -> JobPosting:
        """Return one posting with its description."""
