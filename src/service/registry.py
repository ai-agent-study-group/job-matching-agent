"""RegistryService: 출처별 JobService 목록 (RegistryServicePort 구현)."""

from port.inbound.job import JobServicePort
from port.inbound.registry import RegistryServicePort


class RegistryService(RegistryServicePort):
    """조립할 때 받은 출처별 JobService를 이름으로 들고 있음."""

    def __init__(self, services: dict[str, JobServicePort]):
        self.services = services

    async def list_sources(self) -> list[str]:
        return list(self.services)

    def get(self, name: str) -> JobServicePort:
        if name not in self.services:
            raise ValueError(f"Unknown source '{name}'. Use one of: {', '.join(self.services)}.")
        return self.services[name]
