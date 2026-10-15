"""PoC 실행.

1. LiteLLM 프록시 (API 키는 여기만 필요): poc/litellm.yaml 상단의 명령
2. uv run --group poc python -m poc.run anthropic "research engineer"
   모델 변경: MODEL=sonnet (litellm.yaml의 model_name)
"""

import argparse
import asyncio
import logging
import os

from poc.adapters import load_agent
from poc.domain.models import JobSearch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("board")
    parser.add_argument("role")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--agent", default=os.environ.get("AGENT", "pydantic-ai"))
    args = parser.parse_args()

    logging.basicConfig(format="%(message)s")
    logging.getLogger("poc").setLevel(logging.INFO)

    agent = load_agent(args.agent)
    req = JobSearch(board=args.board, role=args.role, limit=args.limit)
    for posting in asyncio.run(agent.run(req)):
        print(posting.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
