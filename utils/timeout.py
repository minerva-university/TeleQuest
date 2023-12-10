from threading import Thread
from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class TimeoutError(Exception):
    pass


def timeout(timeout: int) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Parameters
    ----------
    timeout: int
        timeout in seconds
    """

    def deco(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            res: list[Exception | T] = [
                TimeoutError(
                    f"function {func.__name__} timeout [{timeout} seconds] exceeded!"
                )
            ]

            def newFunc() -> None:
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e

            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception as je:
                print("error starting thread")
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret

        return wrapper

    return deco
