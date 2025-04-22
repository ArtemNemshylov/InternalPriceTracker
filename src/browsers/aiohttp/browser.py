import aiohttp
from typing import Optional, Dict, Any
from ..base_browser import BaseBrowser

class AiohttpBrowser(BaseBrowser):
    def __init__(
        self,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        use_session: bool = True
    ):
        self._headers = headers or {}
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None
        self._use_session = use_session

    async def __aenter__(self):
        if self._use_session:
            self._session = aiohttp.ClientSession(
                headers=self._headers,
                timeout=self._timeout
            )
        return self

    async def __aexit__(self, *args):
        if self._session:
            await self._session.close()

    async def fetch_html(self, url: str) -> str:
        async with self._get_session().get(url) as response:
            response.raise_for_status()
            return await response.text()

    async def fetch_json_from_api(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def fetch_json_from_element(self, url: str, selector: str = "pre") -> dict:
        raise NotImplementedError("fetch_json_from_element not accepting extracting json from HTML element")

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    def _get_session(self) -> aiohttp.ClientSession:
        if self._use_session and self._session:
            return self._session
        return aiohttp.ClientSession(
            headers=self._headers,
            timeout=self._timeout
        )
