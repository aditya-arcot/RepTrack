from enum import Enum
from typing import Any

from httpx import AsyncClient

from app.core.config import settings


class HttpMethod(str, Enum):
    GET = "get"
    POST = "post"
    DELETE = "delete"
    PUT = "put"
    PATCH = "patch"


async def make_http_request(
    client: AsyncClient,
    *,
    method: HttpMethod,
    endpoint: str,
    headers: dict[str, str] | None = None,
    token: str | None = None,
    data: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
):
    if headers is None:
        headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    if method == HttpMethod.GET:
        return await client.get(endpoint, headers=headers)
    elif method == HttpMethod.POST:
        return await client.post(endpoint, data=data, json=json, headers=headers)
    elif method == HttpMethod.DELETE:
        return await client.delete(endpoint, headers=headers)
    elif method == HttpMethod.PUT:
        return await client.put(endpoint, data=data, json=json, headers=headers)
    else:  # patch
        return await client.patch(endpoint, data=data, json=json, headers=headers)


async def login_and_get_token(
    client: AsyncClient,
    *,
    username: str = settings.ADMIN_USERNAME,
    password: str = settings.ADMIN_PASSWORD,
):
    resp = await make_http_request(
        client,
        method=HttpMethod.POST,
        endpoint="/api/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )
    body = resp.json()
    return body["access_token"]
