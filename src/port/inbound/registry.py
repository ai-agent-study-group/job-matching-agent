"""RegistryServicePort (list_sources · get)."""

from abc import ABC, abstractmethod

from domain.source import Source
from port.inbound.job import JobServicePort


class RegistryServicePort(ABC):
    """MCP 서버 · JMA 앱에 제공하는 출처 목록 기능."""

    @abstractmethod
    async def list_sources(self) -> list[Source]:
        """Name and description of each job source."""

    @abstractmethod
    def get(self, name: str) -> JobServicePort:
        """The service of the source with this name."""
