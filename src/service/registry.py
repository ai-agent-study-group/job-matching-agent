"""RegistryService: 출처별 JobService 목록 (RegistryServicePort 구현)."""

from domain.source import Source
from port.inbound.job import JobServicePort
from port.inbound.registry import RegistryServicePort


class RegistryService(RegistryServicePort):
    """조립할 때 받은 JobService들을 출처 이름으로 들고 있음."""

    def __init__(self, services: list[JobServicePort]):
        names = [service.get_name() for service in services]
        # 이름이 겹치면 딕셔너리에 뒤의 것만 남아 한 출처가 조용히 사라짐
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(
                f"Each source needs its own name, duplicated: {', '.join(duplicates)}."
            )
        self.services = dict(zip(names, services))

    async def list_sources(self) -> list[Source]:
        return [
            Source(name=name, description=service.get_description())
            for name, service in self.services.items()
        ]

    def get(self, name: str) -> JobServicePort:
        if name not in self.services:
            raise ValueError(f"Unknown source '{name}'. Use one of: {', '.join(self.services)}.")
        return self.services[name]
