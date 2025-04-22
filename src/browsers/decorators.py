from functools import wraps
import asyncio
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts+1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        logger.error(f"Max retries ({max_attempts}) exceeded")
                        raise
                    logger.warning(f"Attempt {attempt} failed: {str(e)}")
                    await asyncio.sleep(delay * attempt)
        return wrapper
    return decorator

def timeout(timeout_sec):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=timeout_sec
            )
        return wrapper
    return decorator