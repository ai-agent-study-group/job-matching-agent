"""포트: 모든 어댑터가 구현하는 인터페이스."""

from abc import ABC, abstractmethod

from poc.domain.models import JobPosting, JobSearch


class JobAgent(ABC):
    name: str

    @abstractmethod
    async def run(self, req: JobSearch) -> list[JobPosting]: ...
