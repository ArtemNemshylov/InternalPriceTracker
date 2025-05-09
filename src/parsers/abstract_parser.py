from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class AbstractParser(ABC):
    @staticmethod
    @abstractmethod
    async def fetch_availability(soup: BeautifulSoup) -> bool:
        pass

    @staticmethod
    @abstractmethod
    async def fetch_article(soup: BeautifulSoup) -> str:
        pass

    @staticmethod
    @abstractmethod
    async def fetch_price(soup: BeautifulSoup) -> tuple[float, int | None]:
        pass

