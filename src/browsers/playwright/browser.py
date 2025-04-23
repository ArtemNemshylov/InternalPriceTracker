import json

from playwright.async_api import async_playwright
from src.browsers.base_browser import BaseBrowser

class PlaywrightBrowser(BaseBrowser):
    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self._playwright = None
        self._browser = None
        self._context = None

    async def __aenter__(self):
        await self.launch()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def launch(self):
        """Initialize browser instance"""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox"]
        )
        self._context = await self._browser.new_context()

    async def fetch_html(self, url: str) -> str:
        page = await self._context.new_page()
        await page.goto(url, timeout=self.timeout)
        content = await page.content()
        await page.close()
        return content

    async def fetch_json_from_element(self, url: str, selector: str = "pre") -> dict:
        page = await self._context.new_page()
        await page.goto(url)
        element = await page.wait_for_selector(selector)
        text = await element.text_content()
        return json.loads(text)

    async def fetch_json_from_api(self, url: str) -> dict:
        page = await self._context.new_page()
        await page.goto(url)
        content = await page.content()
        return json.loads(content)

    async def close(self):
        """Cleanup resources in reverse order"""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()