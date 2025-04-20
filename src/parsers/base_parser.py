from abc import ABC, abstractmethod
from typing import List

from loguru import logger

from src.core.dto import ProductDTO


class BaseParser(ABC):
    def __init__(self, urls: List[str]):
        self.urls = urls

    @abstractmethod
    async def fetch_page(self, url: str) -> str:
        pass

    @abstractmethod
    def parse_product(self, page_content: str, url: str) -> ProductDTO:
        pass

    async def run(self) -> List[ProductDTO]:
        products = []
        for url in self.urls:
            try:
                page_content = await self.fetch_page(url)
                product = self.parse_product(page_content, url)
                products.append(product)
            except Exception as e:
                logger.error(f"[ERROR] Failed processing {url}: {e}")
        return products
