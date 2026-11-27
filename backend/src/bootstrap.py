"""앱이 쓸 출처(연방고용청, freehire)를 정하고 준비하는 파일.

MCP 도구는 registry에서 출처를 이름으로 찾아 쓴다. 이 파일은 출처 클라이언트를 만들고,
각각 JobService로 감싸 registry에 넣은 뒤 main.py에 넘긴다.

실제 출처 클래스(ArbeitsagenturClient, FreehireClient)를 아는 곳은 이 파일뿐이다.
그래서 main.py, MCP 서버(server.py), service 코드는 어떤 출처가 붙는지 몰라도 되고,
새 출처를 붙일 때도 bootstrap()에 한 줄만 더하면 된다.

출처 클라이언트는 외부 API와의 HTTP 연결을 열어 두고 계속 다시 쓴다.
main.py는 앱이 켜질 때 Container.open()으로 이 연결을 열고, 앱이 꺼질 때 닫는다.

bootstrap()에 가짜 출처를 넘기면 실제 API를 부르지 않는다 (test/test_bootstrap.py).
Cosmic Python 13장에 나오는 bootstrap 스크립트와 같은 역할이다.
"""

from collections.abc import AsyncGenerator
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass

from adapter.outbound.source.api.arbeitsagentur.client import ArbeitsagenturClient
from adapter.outbound.source.api.freehire.client import FreehireClient
from port.inbound.registry import RegistryServicePort
from port.outbound.source import JobSource
from service.job import JobService
from service.registry import RegistryService


@dataclass
class Container:
    """bootstrap()이 main.py에 돌려주는 것.

    registry는 MCP 도구가 출처를 찾을 때 쓴다. open()은 출처들의 HTTP 연결을 열고, 끝나면 닫는다.
    """

    registry: RegistryServicePort
    clients: list[JobSource]

    @asynccontextmanager
    async def open(self) -> AsyncGenerator[None]:
        async with AsyncExitStack() as stack:
            for client in self.clients:
                await stack.enter_async_context(client)
            yield


def bootstrap(clients: list[JobSource] | None = None) -> Container:
    """출처 클라이언트를 registry에 넣어 Container로 돌려준다. clients가 없으면 연방고용청과 freehire를 쓴다."""
    if clients is None:
        # 실제 출처. 만들기만 하고 연결은 Container.open()에서 엶. 새 출처는 여기에 한 줄 추가
        clients = [ArbeitsagenturClient(), FreehireClient()]
    registry = RegistryService([JobService(client) for client in clients])
    return Container(registry=registry, clients=clients)
