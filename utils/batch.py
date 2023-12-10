from typing import Sequence, TypeVar
from math import ceil

T = TypeVar("T")


def split_into_batches(objects: Sequence[T], batch_size: int) -> list[list[T]]:
    """
    Splits a list of objects into batches of size batch_size.
    ---
    Parameters
        objects: Sequence[T]
                The list of objects to be split into batches.
        batch_size: int
                The size of each batch.
    Returns
        batches: list[list[T]]
                The list of batches of objects.
    """
    if not isinstance(objects, list):
        objects = list(objects)
    num_batches = ceil(len(objects) / batch_size)
    return [objects[i * batch_size : (i + 1) * batch_size] for i in range(num_batches)]
