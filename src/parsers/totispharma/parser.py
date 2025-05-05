import asyncio
from pathlib import Path
from typing import List
from bs4 import BeautifulSoup

from src.core.dto import ProductDTO
from src.parsers.base_parser import BaseParser


class TotisPharmaParser(BaseParser):
    @staticmethod
    async def fetch_name(soup):
        name = soup.find("h1", class_="site-main-title site-main-title--variant_product tt-space_mt tt-space_mt--5-till-xl ds-caption").text.strip()
        return name

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

    async def parse(self, url_list: List[str]) -> List[ProductDTO]:
        products = []
        for url in url_list:
            html = await self.fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            is_available = await self.fetch_availability(soup)
            name = await self.fetch_name(soup)
            price, discount = await self.fetch_price(soup)
            product = ProductDTO(name=name, price=price, available=is_available, discount=discount)
            products.append(product)
        return products



async def main():
    parser = TotisPharmaParser()
    try:
        urls = Path("links.txt").read_text(encoding="utf-8").splitlines()
        products = await parser.parse(urls)
        for product in products:
            print(product.name, product.price, product.available, product.discount)

    finally:
        await parser.close()


if __name__ == "__main__":
    asyncio.run(main())