import asyncio
from pathlib import Path

from src.parsers.base_parser import BaseParser


class TotisPharmaParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    async def fetch_article(soup):
        try:
            article = soup.find(
                "span",
                class_="ds-caption ds-caption--size_4xs ds-caption--size_xs-xl ds-caption--light"
            )
            if article:
                return article.text.split(':')[1].strip()
        except Exception:
            pass
        return ""

    @staticmethod
    async def fetch_availability(soup):
        try:
            out_of_stock = soup.find(
                'span',
                class_="ds-caption ds-caption--size_sm ds-caption--light tt-space_pl"
            )
            return not bool(out_of_stock)
        except Exception:
            return True

    @staticmethod
    async def fetch_price(soup):
        try:
            old_price_tag = soup.find(
                'p',
                class_="ds-caption ds-caption--semibold ds-caption--size_sm ds-caption--size_3md-xl ds-caption--appearance_line-througt ds-caption--color_semigrey js-price-view is-active"
            )
            if old_price_tag:
                old_price = old_price_tag.get("data-price")
                price_tag = soup.find(
                    'p',
                    class_="ds-caption ds-caption--semibold ds-caption--size_3md ds-caption--size_xl-xl js-price-view is-active"
                )
                price = price_tag.get("data-price") if price_tag else old_price
                discount = 100 - (float(old_price) / float(price) * 100)
                return int(float(old_price)), int(discount)

            price_tag = soup.find(
                'p',
                class_="ds-caption ds-caption--size_lg ds-caption--semibold ds-caption--appearance_right ds-caption--appearance_nowrap js-price-view is-active"
            )
            if price_tag:
                price = price_tag.get("data-price")
                return int(float(price)), 0
        except Exception:
            pass
        return 0, 0


async def main():
    parser_dir = Path(__file__).resolve().parent
    links_path = parser_dir / "links.txt"
    parser = TotisPharmaParser(
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
        return products
    finally:
        await parser.close()


if __name__ == "__main__":
    asyncio.run(main())
