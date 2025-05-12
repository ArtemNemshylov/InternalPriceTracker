from pathlib import Path

from src.parsers.registry import PARSER_REGISTRY

async def handle_parse_links(cmd):
    parser_class = PARSER_REGISTRY.get(cmd.parser_name)
    if not parser_class:
        raise ValueError(f"Parser '{cmd.parser_name}' not found.")

    parser = parser_class(browser_type="playwright", browser_config={
        "playwright": {
            "headless": True,
            "timeout": 4500
        }
    })
    try:
        urls = Path(cmd.links_path).read_text(encoding="utf-8").splitlines()
        products = await parser.parse(urls)
        for product in products:
            print(product.article, product.price, product.available, product.discount)
    finally:
        await parser.close()
