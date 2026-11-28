"""인증: /mcp와 /api의 WorkOS 로그인 토큰 검사.

/mcp: AUTHKIT_DOMAIN이 있을 때만 로그인 검사가 붙음. AuthKit 도메인은 가짜 주소.
/api: /api/profile, /api/search는 토큰이 없거나 틀리면 401, /health는 토큰 없이 200.
"""

import asyncio
from types import SimpleNamespace

import httpx2
import pytest
from fastapi.testclient import TestClient
from fastmcp.server.auth.providers.jwt import JWTVerifier, RSAKeyPair

from adapter.inbound.auth import create_api_auth, create_mcp_auth
from adapter.inbound.mcp.server import create_server
from domain.profile import Profile
from main import create_app
from service.registry import RegistryService

DOMAIN = "https://jma-test.authkit.app"
BASE_URL = "https://jma.example.com"
WORKOS_ISSUER = "https://api.workos.com/"
KEY_PAIR = RSAKeyPair.generate()


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


def api_verifier() -> JWTVerifier:
    return JWTVerifier(public_key=KEY_PAIR.public_key, issuer=WORKOS_ISSUER)


def test_no_workos_client_id_means_no_api_auth(monkeypatch):
    """WORKOS_CLIENT_ID가 없으면 /api용 검증기를 만들지 않는다."""
    monkeypatch.delenv("WORKOS_CLIENT_ID", raising=False)

    assert create_api_auth() is None


def test_workos_client_id_creates_jwt_verifier(monkeypatch):
    """WORKOS_CLIENT_ID가 있으면 WorkOS 공개키 주소와 발급자로 JWTVerifier를 만든다."""
    monkeypatch.setenv("WORKOS_CLIENT_ID", "client_123")

    verifier = create_api_auth()

    assert isinstance(verifier, JWTVerifier)
    assert verifier.jwks_uri == "https://api.workos.com/sso/jwks/client_123"
    assert verifier.issuer == WORKOS_ISSUER


@pytest.mark.parametrize(
    ("path", "kwargs"),
    [
        pytest.param("/api/profile", {"data": {"resume": "Data Analyst"}}, id="profile"),
        pytest.param("/api/search", {"json": {"experiences": []}}, id="search"),
    ],
)
def test_api_without_token_is_401(path, kwargs):
    """토큰 없이 /api/profile, /api/search를 부르면 401을 돌려준다."""
    app = create_app(api_auth=api_verifier())

    response = TestClient(app).post(path, **kwargs)

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


@pytest.mark.parametrize(
    "token",
    [
        pytest.param("not-a-jwt", id="malformed"),
        pytest.param(
            KEY_PAIR.create_token(subject="user_123", issuer=WORKOS_ISSUER, expires_in_seconds=-60),
            id="expired",
        ),
        pytest.param(
            KEY_PAIR.create_token(subject="user_123", issuer="https://evil.example.com/"),
            id="wrong-issuer",
        ),
        pytest.param(
            RSAKeyPair.generate().create_token(subject="user_123", issuer=WORKOS_ISSUER),
            id="wrong-key",
        ),
    ],
)
@pytest.mark.parametrize(
    ("path", "kwargs"),
    [
        pytest.param("/api/profile", {"data": {"resume": "Data Analyst"}}, id="profile"),
        pytest.param("/api/search", {"json": {"experiences": []}}, id="search"),
    ],
)
def test_api_with_invalid_token_is_401(path, kwargs, token):
    """깨진·만료된 토큰, 다른 발급자(iss), 다른 서명 키로 만든 토큰은 모두 401을 돌려준다."""
    app = create_app(api_auth=api_verifier())

    response = TestClient(app).post(
        path,
        headers={"Authorization": f"Bearer {token}"},
        **kwargs,
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_api_without_verifier_is_401():
    """api_auth가 없어도 Bearer 토큰을 보낸 /api 요청은 500 대신 401을 돌려준다."""
    app = create_app(api_auth=None)
    token = KEY_PAIR.create_token(subject="user_123", issuer=WORKOS_ISSUER)

    response = TestClient(app).post(
        "/api/profile",
        headers={"Authorization": f"Bearer {token}"},
        data={"resume": "Data Analyst"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_health_without_token_is_200():
    """/health는 같은 라우터에 있어도 토큰 없이 200을 돌려준다."""
    app = create_app(api_auth=api_verifier())

    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_with_valid_token_passes_auth(monkeypatch):
    """유효한 WorkOS 토큰이 있으면 로그인 검사를 통과해 라우트가 실행된다."""
    app = create_app(api_auth=api_verifier())
    token = KEY_PAIR.create_token(subject="user_123", issuer=WORKOS_ISSUER)

    class FakeProfileAgent:
        async def run(self, resume: str):
            return SimpleNamespace(output=Profile())

    monkeypatch.setattr(app.state, "profile_agent", FakeProfileAgent(), raising=False)

    response = TestClient(app).post(
        "/api/profile",
        headers={"Authorization": f"Bearer {token}"},
        data={"resume": "Data Analyst"},
    )

    assert response.status_code == 200
