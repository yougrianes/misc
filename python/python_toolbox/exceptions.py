from loguru import logger
from func_timeout import func_timeout, FunctionTimedOut

from functools import wraps

defaultTimeout = -10000

def try_and_catch_exception(set_timeout=False, timeout=defaultTimeout):
    """a decorator help you catch and manage exception easier.

    usage:
        @try_and_catch_exception(): without timeout
        
        @try_and_catch_exception(set_timeout=True, timeout=(int)): with timeout. if set_timeout is set, timeout param should follow.

    Args:
        timeout (int, optional): refer to pypi module func_timeout. Defaults to None.
    """
    def _function_decorator(func):
        logger.info(f"{func.__name__}: start running")
        def _function_wrapper(*args, **kwargs):
            try:
                if set_timeout == False:
                    result = func(*args, **kwargs)

                elif not isinstance(timeout, int):
                    raise RuntimeError(f"timeout should be an int instance!")

                elif timeout <= 0:
                    raise RuntimeError(f"timeout should greater than 0, and you set timeout = {timeout}...")

                elif timeout > 0:
                    result = func_timeout(timeout, func, args=args, kwargs=kwargs)

            except FunctionTimedOut as timeout_e:
                err_info = f"{func.__name__}: timeout error! info: {timeout_e} "
                logger.error(err_info)
                raise FunctionTimedOut(timeout_e)

            except Exception as e:
                err_info = f"{func.__name__}: error occur! info: {e}"
                logger.error(err_info)
                raise Exception(err_info)

            else:
                logger.info(f"{func.__name__}: succeed")
                return result

        return wraps(func)(_function_wrapper)

    return _function_decorator
