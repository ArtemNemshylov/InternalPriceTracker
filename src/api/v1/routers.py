from pathlib import Path

from fastapi import APIRouter, HTTPException

from src.api.schemas import ParserName
from src.core.messagebus import MessageBus
from src.core.commands import ParseLinks
from src.parsers.registry import PARSER_REGISTRY

router = APIRouter(prefix="/parse", tags=["parsers"])

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

@router.get("/")
async def parse_all():
    bus = MessageBus()
    results = {}

    for parser_name in PARSER_REGISTRY.keys():
        links_path = PROJECT_ROOT / "parsers" / parser_name / "links.txt"
        try:
            await bus.handle(ParseLinks(parser_name=parser_name, links_path=links_path))
            results[parser_name] = "success"
        except Exception as e:
            results[parser_name] = f"error: {str(e)}"

    return results


@router.post("/")
async def parse_one(
        parser_name: ParserName
) -> dict:
    if parser_name not in PARSER_REGISTRY:
        raise HTTPException(status_code=404, detail="Parser not found")

    bus = MessageBus()
    links_path = f"src/parsers/{parser_name}/links.txt"

    try:
        await bus.handle(ParseLinks(parser_name=parser_name.parser, links_path=links_path))
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
