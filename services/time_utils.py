import functools
import logging
import time

logger = logging.getLogger(__name__)

def async_perf_counter(func):
    @functools.wraps(func)
    async def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = await func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        logger.info(f"Elapsed time for function ***{func.__name__.upper()}***: ***{elapsed_time:0.4f}*** seconds")
        return value
    return wrapper_timer