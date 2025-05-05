import asyncio
from typing import Optional, Dict, Any

from .factory import BrowserFactory

class BrowserPool:
    def __init__(self, browser_config: Optional[Dict[str, Dict[str, Any]]] = None):
        self._pools = {
            "playwright": asyncio.Queue(),
            "aiohttp": asyncio.Queue()
        }
        self.config = browser_config or {}

    async def get_browser(self, browser_type: str):
        if self._pools[browser_type].empty():
            browser = await BrowserFactory.create(
                browser_type,
                **self.config.get(browser_type, {})
            )
            return browser
        return await self._pools[browser_type].get()

    async def release(self, browser, browser_type: str):
        await self._pools[browser_type].put(browser)

    async def shutdown(self):
        for pool in self._pools.values():
            while not pool.empty():
                browser = await pool.get()
                await browser.close()
