from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import FileResponse

from src.api.schemas import ParserName
from src.api.v1.parsing_service import (
    get_parser_names,
    run_all_parsers,
    run_one_parser,
    get_excel_path, get_parser_links, save_parser_links,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

router = APIRouter(prefix="/parse", tags=["parsers"])

@router.get("/list")
async def list_parsers():
    return {"parsers": get_parser_names()}

@router.get("/")
async def parse_all():
    return await run_all_parsers()

@router.post("/")
async def parse_one(parser_name: ParserName):
    try:
        return await run_one_parser(parser_name.parser)
    except ValueError:
        raise HTTPException(status_code=404, detail="Parser not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download")
async def download_all():
    file_path = get_excel_path()
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Excel file not found")
    return FileResponse(file_path, filename=file_path.name, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@router.get("/download/{parser_name}")
async def download_single(parser_name: str):
    file_path = get_excel_path(parser_name)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Excel file not found")
    return FileResponse(file_path, filename=file_path.name, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



class LinksUpdate(BaseModel):
    links: str

@router.get("/links/{parser_name}")
async def get_links(parser_name: str):
    try:
        links_text = get_parser_links(parser_name)
        return {"parser": parser_name, "links": links_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/links/{parser_name}")
async def update_links(parser_name: str, data: LinksUpdate):
    try:
        save_parser_links(parser_name, data.links)
        return {"status": "updated", "parser": parser_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

