from .retailer_a.parser import RetailerAParser
from .retailer_b.parser import RetailerBParser
# … імпортуємо інші парсери …

PARSERS = {
    "retailer_a": RetailerAParser(),
    "retailer_b": RetailerBParser(),
    # … та інші …
}
