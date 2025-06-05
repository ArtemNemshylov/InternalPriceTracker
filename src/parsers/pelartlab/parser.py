from bs4 import BeautifulSoup
from pathlib import Path

from src.parsers.base_parser import BaseParser


class PelartlabParser(BaseParser):
    @staticmethod
    async def fetch_article(soup: BeautifulSoup) -> str:
        try:
            article_div = soup.find('div', class_='SDLrh4')
            if article_div:
                article_text = article_div.get_text(strip=True)
                article = article_text.split(':')[1].strip()
                return article
            return ""
        except Exception as e:
            print(f"Error parsing article: {e}")
            return ""

    @staticmethod
    async def fetch_price(soup: BeautifulSoup) -> tuple[float, int]:
        try:
            price_span = soup.find('span', attrs={'data-hook': 'formatted-primary-price'})
            if price_span:
                price_text = price_span.get_text(strip=True)
                price = float(price_text.replace('₴', '').replace(',', '.').replace('\xa0', '').strip())
                return price, 0
            return 0, 1
        except Exception as e:
            print(f"Error parsing price: {e}")
            return 0, 1

    @staticmethod
    async def fetch_availability(soup: BeautifulSoup) -> bool:
        try:
            out_of_stock = soup.find('div', class_='LkMKXj')
            return not bool(out_of_stock)  # True если нет элемента "Немає в наявності"
        except Exception as e:
            print(f"Error parsing availability: {e}")
            return False


async def main():
    current_dir = Path(__file__).parent
    links_file = current_dir / "links.txt"

    parser = PelartlabParser(
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
        print(products)
        return products
    finally:
        await parser.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())