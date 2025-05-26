from src.parsers.decaar import parser as decaar
from src.parsers.lascos import parser as lascos
from src.parsers.pielcosmetics import parser as pielcosmetics
from src.parsers.sesderma import parser as sesderma
from src.parsers.totispharma import parser as totispharma
from src.parsers.christinacosmetics import parser as christinacosmetics
from src.parsers.yudina import parser as yudina

PARSER_REGISTRY = {
    "decaar": decaar.main,
    "lascos": lascos.main,
    "pielcosmetics": pielcosmetics.main,
    "sesderma": sesderma.main,
    "totispharma": totispharma.main,
    "christinacosmetics": christinacosmetics.main,
    "yudina": yudina.main
}
