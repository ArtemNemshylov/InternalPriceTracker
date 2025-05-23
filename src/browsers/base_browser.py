from abc import ABC, abstractmethod

class BaseBrowser(ABC):
    @abstractmethod
    async def fetch_html(self, url: str) -> str:
        pass

    @abstractmethod
    async def fetch_json_from_api(self, url: str) -> dict:
        pass

    @abstractmethod
    async def fetch_json_from_element(self, url: str, selector: str = "pre") -> dict:
        pass

    @abstractmethod
    async def close(self):
        pass