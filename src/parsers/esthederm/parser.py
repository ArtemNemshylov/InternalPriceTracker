from bs4 import BeautifulSoup
from pathlib import Path
from src.parsers.base_parser import BaseParser


class EsthedermParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    async def fetch_price(soup: BeautifulSoup) -> tuple[float, float]:
        try:
            price_element = soup.select_one('.woocommerce-Price-amount.amount')
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Remove currency symbol and spaces, replace comma with dot
                price = float(price_text.replace('грн.', '').replace(' ', '').replace(',', '.').strip())
                return price, 0
            return 0, 0
        except Exception as e:
            print(f"Error parsing price: {e}")
            return 0, 0

    @staticmethod
    async def fetch_availability(soup: BeautifulSoup) -> bool:
        try:
            add_to_cart_button = soup.find('button', class_='single_add_to_cart_button')
            return bool(add_to_cart_button)
        except Exception as e:
            print(f"Error parsing availability: {e}")
            return False

    @staticmethod
    async def fetch_article(soup: BeautifulSoup) -> str:
        try:
            sku_element = soup.select_one('.sku')
            if sku_element:
                return sku_element.get_text(strip=True)
            return "not_found"
        except Exception as e:
            print(f"Error parsing article: {e}")
            return "error"


async def main():
    current_dir = Path(__file__).parent
    links_file = current_dir / "links.txt"
    
    parser = EsthedermParser(
        browser_type="playwright",
        browser_config={
            "playwright": {
                "headless": True,
                "timeout": 45000
            }
        }
    )
    try:
        with open(links_file, "r", encoding="utf-8") as f:
            urls = f.read().splitlines()
        products = await parser.parse(urls)
        return products
    finally:
        await parser.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 