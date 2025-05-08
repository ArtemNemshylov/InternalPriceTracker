from pydantic import BaseModel


class ParserName(BaseModel):
    parser: str
