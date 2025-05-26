import traceback
from datetime import datetime
from pathlib import Path
from src.parsers.registry import PARSER_REGISTRY
from src.core.excel_exporter import ExcelExporter

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

EXPORT_DIR = PROJECT_ROOT / "exports"
EXPORT_DIR.mkdir(exist_ok=True)

def get_parser_names():
    return list(PARSER_REGISTRY.keys())


async def run_all_parsers():
    results = {}
    products = []

    for name, main_func in PARSER_REGISTRY.items():
        try:
            parsed = await main_func()
            if not isinstance(parsed, list):
                results[name] = "invalid result (not a list)"
                continue

            products.extend(parsed)
            results[name] = f"success ({len(parsed)} products)"

        except Exception as e:
            tb = traceback.format_exc()
            results[name] = f"error: {str(e)}"
            results[f"{name}_trace"] = tb

    filename_prefix = "all_parsers"
    today = datetime.now()
    file_path = ExcelExporter.export(products, filename_prefix, EXPORT_DIR)

    return {
        "status": "done",
        "parsers_ran": list(PARSER_REGISTRY.keys()),
        "products_count": len(products),
        "excel": str(file_path.relative_to(PROJECT_ROOT)),
        "download_url": "/parse/download",
        "details": results
    }

async def run_one_parser(name: str):
    if name not in PARSER_REGISTRY:
        raise ValueError("Parser not found")

    func = PARSER_REGISTRY[name]
    products = await func()

    if not products:
        return {"status": "no products", "parser": name}

    file_path = ExcelExporter.export(products, name, EXPORT_DIR)
    return {
        "status": "success",
        "parser": name,
        "products_count": len(products),
        "excel": str(file_path.relative_to(PROJECT_ROOT))
    }

def get_excel_path(parser_name: str | None = None) -> Path:
    today = datetime.now()
    filename = f"{parser_name}_{today.year}_{today.month:02}_{today.day:02}.xlsx" if parser_name else \
               f"all_parsers_{today.year}_{today.month:02}_{today.day:02}.xlsx"
    return EXPORT_DIR / filename

def get_parser_links(parser_name: str) -> str:
    path = PROJECT_ROOT / "parsers" / parser_name / "links.txt"
    print(path)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")

def save_parser_links(parser_name: str, links_text: str) -> None:
    path = PROJECT_ROOT / "parsers" / parser_name / "links.txt"
    path.write_text(links_text.strip(), encoding="utf-8")
