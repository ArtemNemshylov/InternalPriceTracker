PARSER_REGISTRY = {}

def register_parser(name: str):
    def wrapper(cls):
        if name in PARSER_REGISTRY:
            raise ValueError(f"Parser '{name}' is already registered")
        PARSER_REGISTRY[name] = cls
        return cls
    return wrapper
