import asyncio
from pathlib import Path
from bs4 import BeautifulSoup

from src.parsers.base_parser import BaseParser


class EsseskincareParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    async def fetch_price(soup: BeautifulSoup) -> tuple[float, int]:
        try:
            price_box = soup.find("div", class_="product-price__box")
            if price_box:
                new_price_div = price_box.find("div", class_="product-price__item--new")
                old_price_div = price_box.find("div", class_="product-price__old-price")
                if new_price_div and old_price_div:
                    new_price = float(new_price_div.text.replace("грн", "").replace(" ", "").replace(",", ".").strip())
                    old_price = float(old_price_div.text.replace("грн", "").replace(" ", "").replace(",", ".").strip())
                    discount = int(round((old_price - new_price) / old_price * 100))
                    return old_price, discount
                elif new_price_div:
                    price = float(new_price_div.text.replace("грн", "").replace(" ", "").replace(",", ".").strip())
                    return price, 0
            return 0.0, 0
        except Exception as e:
            print(f"Error parsing price: {e}")
            return 0.0, 0

    @staticmethod
    async def fetch_article(soup: BeautifulSoup) -> str:
        try:
            code_div = soup.find("div", class_="product-header__code")
            if code_div:
                spans = code_div.find_all("span")
                if spans:
                    return code_div.text.replace(spans[0].text, "").strip()
            return ""
        except Exception as e:
            print(f"Error parsing article: {e}")
            return ""

    @staticmethod
    async def fetch_availability(soup: BeautifulSoup) -> bool:
        try:
            return bool(soup.find("a", class_="btn __special j-buy-button-add"))
        except Exception as e:
            print(f"Error parsing availability: {e}")
            return False

async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"
    parser = EsseskincareParser(
        browser_type="playwright",
        browser_config={
            "playwright": {
                "headless": True,
                "timeout": 30000
            }
        }
    )
    try:
        urls = links_path.read_text(encoding="utf-8").splitlines()
        products = await parser.parse(urls)
        print(products)
        return products
    finally:
        await parser.close()

if __name__ == "__main__":
    asyncio.run(main())
