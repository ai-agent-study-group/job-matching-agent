"""어댑터 레지스트리. 고른 어댑터만 import해서 다른 프레임워크가 설치돼 있지 않아도 실행됨."""

import importlib

from poc.ports.job_agent import JobAgent

ADAPTERS = {
    "pydantic-ai": "poc.adapters.pydantic_ai_agent:PydanticAIAgent",
}


def load_agent(name: str) -> JobAgent:
    module, cls = ADAPTERS[name].split(":")
    return getattr(importlib.import_module(module), cls)()
