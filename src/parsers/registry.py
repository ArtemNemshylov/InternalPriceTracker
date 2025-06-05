from src.parsers.decaar import parser as decaar
from src.parsers.lascos import parser as lascos
from src.parsers.pielcosmetics import parser as pielcosmetics
from src.parsers.sesderma import parser as sesderma
from src.parsers.totispharma import parser as totispharma
from src.parsers.christinacosmetics import parser as christinacosmetics
from src.parsers.yudina import parser as yudina
from src.parsers.jda import parser as jda
from src.parsers.academie import parser as academie
from src.parsers.esthederm import parser as esthederm
from src.parsers.thalgo import parser as thalgo
from src.parsers.resenss import parser as resenss
from src.parsers.pelartlab import parser as pelartlab

PARSER_REGISTRY = {
    "decaar": decaar.main,
    "lascos": lascos.main,
    "pielcosmetics": pielcosmetics.main,
    "sesderma": sesderma.main,
    "totispharma": totispharma.main,
    "christinacosmetics": christinacosmetics.main,
    "yudina": yudina.main,
    "jda": jda.main,
    "academie": academie.main,
    "esthederm": esthederm.main,
    "thalgo": thalgo.main,
    "resenss": resenss.main,
    "pelartlab": pelartlab.main
}
