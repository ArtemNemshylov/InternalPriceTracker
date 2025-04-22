import asyncio
import json

from playwright.async_api import async_playwright

from src.browsers.base_browser import BaseBrowser


class PlaywrightBrowser(BaseBrowser):
    def __init__(self, headless: bool, timeout: int = 30000, headers: dict | None = None):
        self._headers = headers or {}
        self._headless = headless
        self._timeout = timeout

        self._playwright = None
        self._context = None
        self._browser = None
        self._page = None

    async def __aenter__(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self._headless)
        self._context = await self._browser.new_context(extra_http_headers=self._headers)
        self._page = await self._context.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._page:
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def fetch_html(self, url: str) -> str:
        await self._page.goto(url, timeout=self._timeout)
        return await self._page.content()

    async def fetch_json(self, url: str, selector: str = "pre") -> dict:
        await self._page.goto(url, timeout=self._timeout)
        text = await self._page.inner_text(selector)
        return json.loads(text)

    async def click(self, selector: str):
        await self._page.click(selector)

    async def wait_for(self, selector: str, timeout: int = 5000):
        await self._page.wait_for_selector(selector, timeout=timeout)

    async def scroll_to_bottom(self, delay: float = 0.5, step: int = 500):
        height = await self._page.evaluate("() => document.body.scrollHeight")
        for pos in range(0, height, step):
            await self._page.evaluate(f"window.scrollTo(0, {pos})")
            await asyncio.sleep(delay)


