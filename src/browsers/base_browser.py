from abc import ABC, abstractmethod


class BaseBrowser(ABC):
    @abstractmethod
    async def fetch_html(self, url: str) -> str:
        pass

    @abstractmethod
    async def fetch_json(self, url: str, selector: str = "pre") -> dict:
        pass
