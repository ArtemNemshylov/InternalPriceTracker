import aiohttp

from src.browsers.base_browser import BaseBrowser


class AiohttpBrowser(BaseBrowser):
    def __init__(self, headers: dict | None = None, timeout: int = 30):
        self._headers = headers or {}
        self._timeout = timeout
        self._session = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(headers=self._headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session and not self._session.closed:
            await self._session.close()

    async def fetch_html(self, url: str) -> str:
        async with self._session.get(url, timeout=self._timeout) as response:
            return await response.text()

    async def fetch_json(self, url: str, selector: str = "pre") -> dict:
        async with self._session.get(url, timeout=self._timeout) as response:
            return await response.json()
