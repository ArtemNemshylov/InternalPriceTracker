from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse

from src.api.schemas import ParserName
from src.core.excel_exporter import ExcelExporter
from src.core.messagebus import MessageBus
from src.core.commands import ParseLinks
from src.parsers.registry import PARSER_REGISTRY

router = APIRouter(prefix="/parse", tags=["parsers"])

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

@router.get("/")
async def parse_all():
    bus = MessageBus()
    results = {}
    products = []

    for parser_name, parser_main_func in PARSER_REGISTRY.items():
        try:
            parsed_products = await parser_main_func()
            if parsed_products:
                products.extend(parsed_products)
            results[parser_name] = f"success ({len(parsed_products)} products)"
        except Exception as e:
            results[parser_name] = f"error: {str(e)}"

    # Генерація Excel
    output_dir = PROJECT_ROOT / "exports"
    output_dir.mkdir(exist_ok=True)

    today = datetime.now()
    filename_prefix = "all_parsers"
    file_path = ExcelExporter.export(products, filename_prefix, output_dir)

    results["excel"] = str(file_path.relative_to(PROJECT_ROOT))
    results["products_count"] = len(products)
    results["download_url"] = "/parse/download"

    return results


@router.post("/")
async def parse_one(parser_name: ParserName) -> dict:
    name = parser_name.parser

    if name not in PARSER_REGISTRY:
        raise HTTPException(status_code=404, detail="Parser not found")

    parser_main_func = PARSER_REGISTRY[name]

    try:
        # запускаємо парсер
        products = await parser_main_func()

        if not products:
            return {"status": "no products", "parser": name}

        # зберігаємо Excel
        output_dir = PROJECT_ROOT / "exports"
        output_dir.mkdir(exist_ok=True)
        file_path = ExcelExporter.export(products, name, output_dir)

        return {
            "status": "success",
            "parser": name,
            "products_count": len(products),
            "excel": str(file_path.relative_to(PROJECT_ROOT))
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download")
async def download_excel():
    output_dir = PROJECT_ROOT / "exports"
    today = datetime.now()
    filename = f"all_parsers_{today.year}_{today.month:02}_{today.day:02}.xlsx"
    file_path = output_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Excel file not found")

    return FileResponse(path=file_path, filename=filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@router.get("/download/{parser_name}")
async def download_parser_excel(parser_name: str):
    output_dir = PROJECT_ROOT / "exports"
    today = datetime.now()
    filename = f"{parser_name}_{today.year}_{today.month:02}_{today.day:02}.xlsx"
    file_path = output_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Excel file not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@router.get("/list")
async def get_parser_list():
    return {"parsers": list(PARSER_REGISTRY.keys())}