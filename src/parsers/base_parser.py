# src/parsers/base_parser.py

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging
from src.browsers.pool import BrowserPool
from src.browsers.base_browser import BaseBrowser

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    def __init__(
        self,
        browser_type: str = "playwright",
        max_retries: int = 3,
        request_timeout: int = 30,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.browser_type = browser_type
        self.max_retries = max_retries
        self.request_timeout = request_timeout
        self.headers = headers or {}
        self.browser_pool = BrowserPool()

    @abstractmethod
    async def parse(self, url: str) -> Any:
        pass

    async def fetch_html(self, url: str) -> str:
        return await self._with_browser(lambda b: b.fetch_html(url))

    async def fetch_json(self, url: str) -> dict:
        return await self._with_browser(lambda b: b.fetch_json_from_api(url))

    async def fetch_json_from_element(self, url: str, selector: str = "pre") -> dict:
        return await self._with_browser(lambda b: b.fetch_json_from_element(url, selector))

    async def _with_browser(self, func):
        for attempt in range(1, self.max_retries + 1):
            browser = await self.browser_pool.get_browser(self.browser_type)
            try:
                return await func(browser)
            except Exception as e:
                logger.warning(f"[{self.browser_type}] Attempt {attempt} failed: {e}")
                if attempt == self.max_retries:
                    raise
            finally:
                await self.browser_pool.release(browser, self.browser_type)

    async def close(self):
        await self.browser_pool.shutdown()
