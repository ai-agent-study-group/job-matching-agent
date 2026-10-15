"""pydantic-ai 어댑터. 도구는 MCP stdio 서버, 모델은 LiteLLM 프록시의 MODEL 별칭."""

import logging
import os
from pathlib import Path

from pydantic_ai import Agent, UsageLimits
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.messages import ToolCallPart
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.litellm import LiteLLMProvider

from poc.domain.models import JobPosting, JobSearch
from poc.ports.job_agent import JobAgent

MCP_SERVER = Path(__file__).parents[1] / "mcp_server.py"
LITELLM_PROXY = os.environ.get("LITELLM_PROXY", "http://127.0.0.1:4000")

INSTRUCTIONS = """\
Greenhouse 보드에서 요청한 직무에 맞는 공고를 찾아 구조화한다.
list_jobs로 후보를 찾고, 관련도가 높은 공고만 get_job으로 읽는다.
요건 문구는 공고 원문 언어 그대로 쓰고, 본문에 없는 내용은 추측하지 않고 비워 둔다.
"""

log = logging.getLogger(__name__)


class PydanticAIAgent(JobAgent):
    name = "pydantic-ai"

    def __init__(self):
        self.agent = Agent(
            OpenAIChatModel(  # 프록시가 OpenAI 호환 API라 OpenAI 모델 클래스로 호출
                os.environ.get("MODEL", "haiku"),  # poc/litellm.yaml의 model_name
                provider=LiteLLMProvider(api_base=LITELLM_PROXY),
            ),
            toolsets=[MCPToolset(MCP_SERVER)],  # .py 경로를 주면 stdio 서브프로세스로 실행
            output_type=list[JobPosting],
            instructions=INSTRUCTIONS,
        )

    async def run(self, req: JobSearch) -> list[JobPosting]:
        result = await self.agent.run(
            f"보드: {req.board}\n직무: {req.role}\n최대 {req.limit}개",
            usage_limits=UsageLimits(request_limit=10),
        )
        for msg in result.all_messages():
            for part in msg.parts:
                if isinstance(part, ToolCallPart):
                    log.info("tool %s %s", part.tool_name, part.args)
        log.info("usage %s", result.usage)
        return result.output
