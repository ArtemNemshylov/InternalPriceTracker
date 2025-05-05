from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import logging
from functools import wraps
from src.browsers.pool import BrowserPool

logger = logging.getLogger(__name__)

def handle_parsing_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Помилка парсингу: {str(e)}")
            raise
    return wrapper

class BaseParser(ABC):
    def __init__(
        self,
        browser_type: str = "playwright",
        request_timeout: int = 30,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.browser_type = browser_type
        self.request_timeout = request_timeout
        self.headers = headers or {}
        self.browser_pool = BrowserPool()

    @abstractmethod
    @handle_parsing_errors
    async def parse(self, url_list: List[str]) -> List[Any]:
        pass

    async def fetch_html(self, url: str) -> str:
        browser = await self.browser_pool.get_browser(self.browser_type)
        try:
            return await browser.fetch_html(url)
        finally:
            await self.browser_pool.release(browser, self.browser_type)

    async def close(self):
        await self.browser_pool.shutdown()