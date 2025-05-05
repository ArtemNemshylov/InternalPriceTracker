# src/browsers/factory.py
from .playwright.browser import PlaywrightBrowser
from .aiohttp.browser import AiohttpBrowser
from .base_browser import BaseBrowser

class BrowserFactory:
    @staticmethod
    async def create(browser_type: str, **kwargs) -> BaseBrowser:
        if browser_type == "playwright":
            browser = PlaywrightBrowser(**kwargs)
            await browser.launch()
            return browser
        elif browser_type == "aiohttp":
            return AiohttpBrowser(**kwargs)
        raise ValueError(f"Unknown browser type: {browser_type}")