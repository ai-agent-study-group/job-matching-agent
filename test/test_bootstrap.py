"""bootstrap.py: 출처를 서비스에 끼우고, 출처 연결을 열고 닫기.

bootstrap()에 열고 닫을 때 기록만 남기는 가짜 출처를 넘겨서 네트워크를 쓰지 않음.
"""

import asyncio

import pytest

from bootstrap import bootstrap


class RecordingSource:
    """열기 · 닫기를 events에 남기는 출처. fail이면 열기에서 오류를 냄."""

    def __init__(self, label, events, fail=False):
        self.label = label
        self.events = events
        self.fail = fail

    async def __aenter__(self):
        if self.fail:
            raise RuntimeError(f"cannot open {self.label}")
        self.events.append(f"open {self.label}")
        return self

    async def __aexit__(self, *exc):
        self.events.append(f"close {self.label}")

    def name(self):
        return self.label

    def description(self):
        return f"{self.label} postings"


def open_and_close(container, events):
    async def main():
        async with container.open():
            events.append("running")

    asyncio.run(main())


def test_registry_has_the_given_sources():
    """넘긴 출처가 이름 그대로 registry에 들어간다.

    목적: 도구는 registry에서 이름으로 출처를 찾음.
    기대 결과: list_sources가 넘긴 순서대로 이름을 돌려줌.
    """
    container = bootstrap([RecordingSource(label, []) for label in ("a", "b")])

    sources = asyncio.run(container.registry.list_sources())

    assert [source.name for source in sources] == ["a", "b"]


def test_open_opens_in_order_and_closes_in_reverse():
    """출처를 등록 순서대로 열고, 끝나면 반대 순서로 닫는다.

    목적: 앱이 떠 있는 동안 출처 연결을 열어 두고, 꺼질 때 빠짐없이 닫음.
    기대 결과: a 열기 → b 열기 → 실행 → b 닫기 → a 닫기.
    """
    events = []
    container = bootstrap([RecordingSource(label, events) for label in ("a", "b")])

    open_and_close(container, events)

    assert events == ["open a", "open b", "running", "close b", "close a"]


def test_open_failure_closes_already_opened_sources():
    """출처 하나가 열기에 실패하면 이미 연 출처는 닫고 오류를 그대로 낸다.

    목적: 앱 시작이 실패해도 앞서 연 HTTP 연결이 남지 않게 함.
    기대 결과: a 열기 → b 실패 → a 닫기, 그리고 b의 RuntimeError.
    """
    events = []
    container = bootstrap(
        [
            RecordingSource("a", events),
            RecordingSource("b", events, fail=True),
        ]
    )

    with pytest.raises(RuntimeError, match="cannot open b"):
        open_and_close(container, events)

    assert events == ["open a", "close a"]
