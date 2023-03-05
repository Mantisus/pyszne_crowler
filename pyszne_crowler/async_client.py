import asyncio

import httpx

from .config import API_CONCURRENTS, BASE_HEADERS, NAVIGATE_CONCURRENTS


class AsyncHTTPClient:
    def __init__(self):
        limits = httpx.Limits(max_keepalive_connections=10)
        self.navigate_lock = asyncio.Semaphore(NAVIGATE_CONCURRENTS)
        self.api_lock = asyncio.Semaphore(API_CONCURRENTS)
        self.session = httpx.AsyncClient(headers=BASE_HEADERS, limits=limits)

    async def request(self, method: str, url: str, *args, **kwargs) -> httpx.Response:
        return await self.session.request(method, url, timeout=20, *args, **kwargs)

    async def get(self, url: str, *args, **kwargs) -> httpx.Response:
        return await self.request("GET", url, *args, **kwargs)

    async def post(self, url: str, *args, **kwargs) -> httpx.Response:
        return await self.request("POST", url, *args, **kwargs)

    async def close(self) -> None:
        await self.session.aclose()
