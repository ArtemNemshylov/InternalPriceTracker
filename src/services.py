from src.parsers.registry import PARSERS

class ParserService:
    def run_parser(self, name: str):
        parser = PARSERS[name]
        return parser.run()
