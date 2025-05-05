import asyncio
from .factory import BrowserFactory

class BrowserPool:
    def __init__(self, max_browsers=3):
        self._pools = {
            "playwright": asyncio.Queue(max_browsers),
            "aiohttp": asyncio.Queue(max_browsers)
        }

    async def get_browser(self, browser_type: str):
        if self._pools[browser_type].empty():
            browser = await BrowserFactory.create(browser_type, headless=True)
            return browser
        return await self._pools[browser_type].get()

    async def release(self, browser, browser_type: str):
        await self._pools[browser_type].put(browser)

    async def shutdown(self):
        for pool in self._pools.values():
            while not pool.empty():
                browser = await pool.get()
                await browser.close()
