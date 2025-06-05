from bs4 import BeautifulSoup
from pathlib import Path
from src.parsers.base_parser import BaseParser
import requests
from datetime import datetime


class ResenssParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.euro_rate = self.get_euro_rate()

    @staticmethod
    def get_euro_rate() -> float:
        try:
            response = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&json')
            if response.status_code == 200:
                data = response.json()
                return float(data[0]['rate'])
            return 48.0  
        except Exception as e:
            print(f"Error fetching EUR rate: {e}")
            return 48.0 

    @staticmethod
    def _extract_article(text: str) -> str:
        try:
            return text.replace('Article', '').replace(':', '').strip()
        except Exception:
            return "not_found"

    @staticmethod
    async def fetch_availability(soup: BeautifulSoup) -> bool:
        try:
            add_to_cart_button = soup.find('button', id='AddToCart')
            if add_to_cart_button and add_to_cart_button.get('disabled'):
                return False
            return True
        except Exception as e:
            print(f"Error parsing availability: {e}")
            return False

    async def fetch_price(self, soup: BeautifulSoup) -> tuple[float, float]:
        try:
            price_element = soup.select_one('.money-resens')
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Check if price is in EUR or UAH
                if '€' in price_text:
                    price_eur = float(price_text.replace('€', '').strip())
                    price_uah = round(price_eur * self.euro_rate, 2)
                else:
                    price_uah = float(price_text.replace('₴', '').strip())
                return price_uah, 0
            return 0, 0
        except Exception as e:
            print(f"Error parsing price: {e}")
            return 0, 0

    @staticmethod
    async def fetch_article(soup: BeautifulSoup) -> str:
        try:
            # Find div with class text-link-animated and get its first p tag
            article_div = soup.find('div', class_='text-link-animated')
            if article_div:
                article_p = article_div.find('p')
                if article_p:
                    article_text = article_p.get_text(strip=True)
                    article = article_text.split(':')[1].strip()
                    article = article.replace(' ', '').upper()

                    if len(article) <= 6:
                        return article
            return ""
        except Exception as e:
            print(f"Error parsing article: {e}")
            return ""


async def main():
    current_dir = Path(__file__).parent
    links_file = current_dir / "links.txt"
    
    parser = ResenssParser(
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