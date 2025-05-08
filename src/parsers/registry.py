from src.parsers.decaar.parser import DecaarParser
from src.parsers.lascos.parser import LascosParser
from src.parsers.pielcosmetics.parser import PielCosmeticsParser
from src.parsers.sesderma.parser import SesDermaParser

PARSER_REGISTRY = {
    "decaar": DecaarParser,
    "lascos": LascosParser,
    "pielcosmetics": PielCosmeticsParser,
    "sesderma": SesDermaParser,
}
