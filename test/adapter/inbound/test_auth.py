"""인증: AUTHKIT_DOMAIN이 있을 때만 /mcp에 로그인 검사가 붙음.

서버를 띄우지 않고 httpx2.ASGITransport로 MCP 앱에 바로 요청을 보냄.
AuthKit 도메인은 가짜 주소. 토큰 없는 요청은 공개키를 받으러 가기 전에 막혀서 네트워크를 쓰지 않음.
"""

import asyncio

import httpx2
import pytest

from adapter.inbound.auth import create_mcp_auth
from adapter.inbound.mcp.server import create_server
from service.registry import RegistryService

DOMAIN = "https://jma-test.authkit.app"
BASE_URL = "https://jma.example.com"


def request(method: str, path: str, **kwargs) -> httpx2.Response:
    """인증을 붙인 MCP 앱에 요청 하나를 보낸다."""
    app = create_server(RegistryService([]), auth=create_mcp_auth()).http_app(path="/mcp")

    async def main():
        transport = httpx2.ASGITransport(app=app)
        async with httpx2.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.request(method, path, **kwargs)

    return asyncio.run(main())


@pytest.fixture
def authkit_env(monkeypatch):
    monkeypatch.setenv("AUTHKIT_DOMAIN", DOMAIN)
    monkeypatch.setenv("BASE_URL", BASE_URL)


def test_no_authkit_domain_means_no_auth(monkeypatch):
    """AUTHKIT_DOMAIN이 없으면 인증을 붙이지 않는다.

    목적: 로컬 실행과 테스트는 WorkOS 설정 없이 지금처럼 돌아야 함.
    """
    monkeypatch.delenv("AUTHKIT_DOMAIN", raising=False)

    assert create_mcp_auth() is None


def test_authkit_domain_without_base_url_fails(monkeypatch):
    """AUTHKIT_DOMAIN만 있고 BASE_URL이 없으면 앱이 뜨지 않는다.

    목적: 토큰 대상(aud)을 정할 수 없는 채로 배포되지 않게 함.
    """
    monkeypatch.setenv("AUTHKIT_DOMAIN", DOMAIN)
    monkeypatch.delenv("BASE_URL", raising=False)

    with pytest.raises(KeyError):
        create_mcp_auth()


@pytest.mark.usefixtures("authkit_env")
def test_mcp_without_token_is_401():
    """토큰 없이 /mcp를 부르면 401과 함께 로그인 안내 주소를 돌려준다.

    목적: 커넥터는 이 응답의 안내 주소를 보고 로그인 창을 띄움.
    """
    response = request("POST", "/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "initialize"})

    assert response.status_code == 401
    assert (
        f'resource_metadata="{BASE_URL}/.well-known/oauth-protected-resource/mcp"'
        in response.headers["www-authenticate"]
    )


@pytest.mark.usefixtures("authkit_env")
def test_protected_resource_metadata_points_to_authkit():
    """안내 주소는 토큰 대상(BASE_URL/mcp)과 로그인할 AuthKit 도메인을 알려 준다.

    목적: 커넥터가 어디서 로그인할지 이 응답으로 정함. 토큰 없이 열려 있어야 함.
    """
    response = request("GET", "/.well-known/oauth-protected-resource/mcp")

    assert response.status_code == 200
    assert response.json()["resource"] == f"{BASE_URL}/mcp"
    assert response.json()["authorization_servers"] == [DOMAIN]
