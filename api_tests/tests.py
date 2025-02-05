import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app
from test_notice.models import init_mongo
from test_notice.models.auth import User
from test_notice.models.enums import UserRoles
from test_notice.models.notice import Notice
from test_notice.dependencies.auth import get_auth_service


client = TestClient(app)


@pytest_asyncio.fixture
async def test_db():
    await init_mongo()


@pytest_asyncio.fixture
async def test_user(test_db):
    user = User(username="testuser", hashed_password="$2b$12$gLzhLocR5ml.fHq9MbDYmOfnMhWRQVB.2XO9x4VR2159J5c0PCiei", role=UserRoles.user)
    await user.insert()
    yield user
    await user.delete()


@pytest_asyncio.fixture
async def test_admin(test_db):
    user = User(username="testadmin", hashed_password="$2b$12$gLzhLocR5ml.fHq9MbDYmOfnMhWRQVB.2XO9x4VR2159J5c0PCiei", role=UserRoles.admin)
    await user.insert()
    yield user
    await user.delete()


@pytest_asyncio.fixture
async def test_notice(test_db, test_user):
    notice = Notice(title="Test Notice", body="This is a test notice.", user_id=str(test_user.id))
    await notice.insert()
    yield notice
    await notice.delete()


@pytest_asyncio.fixture
async def auth_headers(test_user):
    auth_service = await get_auth_service()
    token = await auth_service.login(test_user.username, "string")
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def admin_auth_headers(test_admin):
    auth_service = await get_auth_service()
    token = await auth_service.login(test_admin.username, "string")
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_register_user(test_db):
    response = client.post("/oauth/register", data={
        "username": "testuser",
        "password": "string"
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login(test_db):
    response = client.post("/oauth/token", data={
        "username": "testuser",
        "password": "string"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_create_notice(auth_headers):
    response = client.put("/notices/", json={
        "title": "Test Notice",
        "body": "This is a test notice."
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Notice"


@pytest.mark.asyncio
async def test_get_notices(auth_headers):
    response = client.get("/notices/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_notice(auth_headers, test_notice):
    response = client.get(f"/notices/{test_notice.id}", headers=auth_headers)
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_patch_notice(auth_headers, test_notice):
    response = client.patch(f"/notices/{test_notice.id}", json={
        "title": "Updated Notice",
        "body": "Updated content."
    }, headers=auth_headers)
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_delete_notice(auth_headers, test_notice):
    response = client.delete(f"/notices/{test_notice.id}", headers=auth_headers)
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_get_admin_notices(admin_auth_headers):
    response = client.get("/admin/notices", headers=admin_auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_admin_notice(admin_auth_headers, test_notice):
    response = client.get(f"/admin/notices/{test_notice.id}", headers=admin_auth_headers)
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_restore_notice(admin_auth_headers, test_notice):
    response = client.patch(f"/admin/notices/{test_notice.id}/restore", headers=admin_auth_headers)
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_get_user_notices(admin_auth_headers, test_user):
    response = client.get(f"/admin/users/{test_user.id}/notices", headers=admin_auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
