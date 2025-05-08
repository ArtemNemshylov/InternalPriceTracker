from src.core.commands import ParseLinks
from src.core.handlers import handle_parse_links

class MessageBus:
    def __init__(self):
        self.handlers = {
            ParseLinks: handle_parse_links,
        }

    async def handle(self, command):
        handler = self.handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler found for command {type(command).__name__}")
        return await handler(command)
