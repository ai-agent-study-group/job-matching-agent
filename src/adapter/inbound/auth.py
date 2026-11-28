"""인증: /mcp와 /api에 붙이는 WorkOS 로그인 토큰 검사.

/mcp: claude.ai · ChatGPT 커넥터는 AuthKit에서 로그인해 받은 토큰을 붙여 /mcp를 부름.
서버는 그 토큰이 AuthKit이 발급한 것인지, 대상(aud)이 BASE_URL/mcp인지 확인함.
/api: JMA 앱이 WorkOS에서 받아 온 로그인 토큰의 서명(JWKS)과 발급자(iss)를 확인함.
"""

import os
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastmcp.server.auth import AccessToken, TokenVerifier
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.auth.providers.workos import AuthKitProvider

_bearer = HTTPBearer()


def create_mcp_auth() -> AuthKitProvider | None:
    # AUTHKIT_DOMAIN이 없으면 인증 없이 열림 (로컬 실행 · 테스트).
    # 배포에서는 https://까지 넣을 것 (예: https://jma.authkit.app). 없으면 URL 파싱 오류로 서버가 뜨지 않음
    domain = os.environ.get("AUTHKIT_DOMAIN")
    if not domain:
        return None
    # BASE_URL은 서버의 공개 https 주소 (예: https://job-matching-agent.fly.dev)
    return AuthKitProvider(authkit_domain=domain, base_url=os.environ["BASE_URL"])


def create_api_auth() -> JWTVerifier | None:
    # WORKOS_CLIENT_ID가 없으면 검증기를 만들지 않음 (/health · /mcp는 그대로 동작, /api는 401로 막힘)
    client_id = os.environ.get("WORKOS_CLIENT_ID")
    if not client_id:
        return None
    return JWTVerifier(
        jwks_uri=f"https://api.workos.com/sso/jwks/{client_id}",
        issuer="https://api.workos.com/",
    )


async def current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
) -> AccessToken:
    """Authorization Bearer 토큰을 검사해 로그인한 사용자를 돌려준다."""
    verifier: TokenVerifier | None = getattr(request.app.state, "api_auth", None)
    token = await verifier.verify_token(credentials.credentials) if verifier else None
    if token is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
