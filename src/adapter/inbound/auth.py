"""인증: /mcp에 붙이는 WorkOS AuthKit 로그인 검사.

claude.ai · ChatGPT 커넥터는 AuthKit에서 로그인해 받은 토큰을 붙여 /mcp를 부름.
서버는 그 토큰이 AuthKit이 발급한 것인지, 대상(aud)이 BASE_URL/mcp인지 확인함.
"""

import os

from fastmcp.server.auth.providers.workos import AuthKitProvider


def create_mcp_auth() -> AuthKitProvider | None:
    # AUTHKIT_DOMAIN이 없으면 인증 없이 열림 (로컬 실행 · 테스트). 배포에서는 꼭 넣을 것
    domain = os.environ.get("AUTHKIT_DOMAIN")
    if not domain:
        return None
    # BASE_URL은 서버의 공개 https 주소 (예: https://job-matching-agent.fly.dev)
    return AuthKitProvider(authkit_domain=domain, base_url=os.environ["BASE_URL"])
