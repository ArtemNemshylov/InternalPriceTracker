from bs4 import BeautifulSoup
from pathlib import Path
from src.parsers.base_parser import BaseParser


class AcademieParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    async def fetch_price(soup: BeautifulSoup) -> tuple[float, float]:
        try:
            add2cart = soup.find("div", class_="add2cart")
            if add2cart:
                price_span = add2cart.find("span", class_="price nowrap")
                if price_span:
                    price_text = price_span.get_text(strip=True)
                    price = float(price_text.replace('грн.', '').replace(' ', '').strip())
                    return price, 0
            return 0, 0
        except Exception as e:
            print(f"Error parsing price: {e}")
            return 0, 0

    @staticmethod
    async def fetch_availability(soup: BeautifulSoup) -> bool:
        try:
            stock_none = soup.select_one('.stock-none')
            return not bool(stock_none)
        except Exception as e:
            print(f"Error parsing availability: {e}")
            return False

    @staticmethod
    async def fetch_article(soup: BeautifulSoup) -> str:
        try:
            article_row = soup.find('td', class_='name', string='Артикул:')
            if article_row:
                article_value = article_row.find_next_sibling('td', class_='value')
                if article_value:
                    return article_value.get_text(strip=True)
            return "not_found"
        except Exception as e:
            print(f"Error parsing article: {e}")
            return "error"


async def main():
    current_dir = Path(__file__).parent
    links_file = current_dir / "links.txt"
    
    parser = AcademieParser(
        browser_type="playwright",
        browser_config={
            "playwright": {
                "headless": True,
                "timeout": 30000
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