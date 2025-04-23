from functools import wraps

def auto_close_page(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        page = await self._context.new_page()
        try:
            return await func(self, page, *args, **kwargs)
        finally:
            await page.close()
    return wrapper

def handle_modal(accept=True):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            page = kwargs.get('page') or args[1]
            page.on('dialog', lambda dialog: dialog.accept() if accept else dialog.dismiss())
            return await func(self, *args, **kwargs)
        return wrapper
    return decorator