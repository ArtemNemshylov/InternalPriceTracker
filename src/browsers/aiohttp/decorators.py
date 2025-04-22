from functools import wraps

def cache_responses(ttl=60):
    def decorator(func):
        cache = {}
        @wraps(func)
        async def wrapper(self, url, *args, **kwargs):
            if url in cache:
                return cache[url]
            result = await func(self, url, *args, **kwargs)
            cache[url] = result
            return result
        return wrapper
    return decorator