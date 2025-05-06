import asyncio
from pathlib import Path

from src.parsers.base_parser import BaseParser


class TotisPharmaParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    @staticmethod
    async def fetch_article(soup):
        article = soup.find("span", class_="ds-caption ds-caption--size_4xs ds-caption--size_xs-xl ds-caption--light").text.split(':')[1].strip()
        return article

    @staticmethod
    async def fetch_availability(soup):
        if soup.find('span', class_="ds-caption ds-caption--size_sm ds-caption--light tt-space_pl"):
            return False
        return True


    @staticmethod
    async def fetch_price(soup):
        old_price = soup.find('p', class_="ds-caption ds-caption--semibold ds-caption--size_sm ds-caption--size_3md-xl ds-caption--appearance_line-througt ds-caption--color_semigrey js-price-view is-active")
        price = soup.find('p', class_="ds-caption ds-caption--size_lg ds-caption--semibold ds-caption--appearance_right ds-caption--appearance_nowrap js-price-view is-active")
        if old_price:
            old_price = old_price.get("data-price")
            price = soup.find('p', class_="ds-caption ds-caption--semibold ds-caption--size_3md ds-caption--size_xl-xl js-price-view is-active").get("data-price")
            discount = 100 - (float(old_price) / float(price) * 100)
            price = int(float(price))
            discount = int(discount)
            return price, discount
        price = price.get("data-price")
        price = int(float(price))
        return price, 0


async def main():
    parser = TotisPharmaParser(
        browser_type="playwright",
        browser_config={
            "playwright": {
                "headless": True,
                "timeout": 4500
            }
        }
    )
    try:
        urls = Path("links.txt").read_text(encoding="utf-8").splitlines()
        products = await parser.parse(urls[:2])
        for product in products:
            print(product.article, product.price, product.available, product.discount) # заглушка, потом подумаем чо з єтой хуетой делать
    finally:
        await parser.close()


if __name__ == "__main__":
    asyncio.run(main())