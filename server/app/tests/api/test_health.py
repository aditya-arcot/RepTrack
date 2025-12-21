from httpx import AsyncClient


async def test_health(client: AsyncClient):
    resp = await client.get("/api/health")

    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "success"
    assert body["code"] == "HEALTH_OK"
    assert body["message"] == "ok"
    data = body["data"]
    assert data is None
