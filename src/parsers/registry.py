from src.parsers.decaar import parser as decaar
from src.parsers.lascos import parser as lascos
from src.parsers.pielcosmetics import parser as pielcosmetics
from src.parsers.sesderma import parser as sesderma
from src.parsers.totispharma import parser as totispharma

PARSER_REGISTRY = {
    "decaar": decaar.main,
    "lascos": lascos.main,
    "pielcosmetics": pielcosmetics.main,
    "sesderma": sesderma.main,
    "totispharma": totispharma.main
}
