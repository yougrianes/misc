from loguru import logger
from func_timeout import func_timeout, FunctionTimedOut

from functools import wraps

def try_and_catch_exception(timeout=None):
    """a decorator help you catch and manage exception easier.

    Args:
        timeout (int, optional): refer to pypi module func_timeout. Defaults to None.
    """
    def _function_decorator(func):
        logger.info(f"{func.__name__}: start running")
        def _function_wrapper(*args, **kwargs):
            try:
                if timeout is None:
                    result = func(*args, **kwargs)
                elif not isinstance(timeout,int):
                    raise RuntimeError(f"timeout should be an int instance!")
                elif timeout > 0:
                    result = func_timeout(timeout, func, args=args, kwargs=kwargs)
                elif timeout <= 0:
                    raise RuntimeError(f"timeout should greater than 0, and you set timeout = {timeout}...")
                else:
                    raise RuntimeError(f"unknown error occured...")
            except FunctionTimedOut as e:
                err_info = f"{func.__name__}: timeout error! info: {e} "
                logger.error(err_info)
                raise RuntimeError(err_info)
            except Exception as e:
                err_info = f"{func.__name__}: error occur! info: {e}"
                logger.error(err_info)
                raise RuntimeError(err_info)
            else:
                logger.info(f"{func.__name__}: succeed")
                return result
        return wraps(func)(_function_wrapper)

    return _function_decorator
