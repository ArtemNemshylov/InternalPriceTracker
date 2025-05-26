import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import logging
from functools import wraps

from bs4 import BeautifulSoup

from src.browsers.pool import BrowserPool
from src.core.dto import ProductDTO

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
        browser_config: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        self.browser_type = browser_type
        self.request_timeout = request_timeout
        self.headers = headers or {}
        self.browser_pool = BrowserPool(browser_config=browser_config or {})

    @staticmethod
    @abstractmethod
    async def fetch_availability(soup):
        pass

    @staticmethod
    @abstractmethod
    async def fetch_article(soup):
        pass

    @staticmethod
    @abstractmethod
    async def fetch_price(soup):
        pass

    @handle_parsing_errors
    async def parse(self, url_list: List[str], num_workers: int = 2) -> List[ProductDTO]:
        chunk_size = max(1, len(url_list) // num_workers)
        chunks = [url_list[i * chunk_size:(i + 1) * chunk_size] for i in range(num_workers)]
        chunks.append(url_list[num_workers * chunk_size:])

        tasks = [
            self._parse_chunk(chunk, i)
            for i, chunk in enumerate(chunks) if chunk
        ]

        results = await asyncio.gather(*tasks)

        all_products = []
        for part in results:
            all_products.extend(part)

        return all_products

    async def _parse_chunk(self, urls: List[str], index: int) -> List[ProductDTO]:
        products = []
        browser = await self.browser_pool.get_browser(self.browser_type)
        try:
            for url in urls:
                html = await browser.fetch_html(url)
                soup = BeautifulSoup(html, "html.parser")
                is_available = await self.fetch_availability(soup)
                article = await self.fetch_article(soup)
                price, discount = await self.fetch_price(soup)
                product = ProductDTO(article=article, price=price, available=is_available, discount=discount, url=url)
                products.append(product)
        except Exception as e:
            logger.error(f"[Worker-{index}] Error: {e}")
        finally:
            await self.browser_pool.release(browser, self.browser_type)
        return products

    async def fetch_html(self, url: str) -> str:
        browser = await self.browser_pool.get_browser(self.browser_type)
        try:
            return await browser.fetch_html(url)
        finally:
            await self.browser_pool.release(browser, self.browser_type)

    async def close(self):
        await self.browser_pool.shutdown()

