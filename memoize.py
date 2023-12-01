"""Contains the memoize decorator needed to prune non-starter prefixes early in the search."""
import functools
from typing import Callable


def memoize_prefix(func: Callable[[str], bool]) -> Callable[[str], bool]:
    """Implements a memoization decorator for the is_valid_prefix function."""

    prefix_cache = {}

    @functools.wraps(func)
    def process_prefix(*args, **kwargs) -> bool:
        prefix = args[0]
        print(f"Checking prefix: {prefix}")
        for i in range(len(prefix) + 1):
            sub_prefix = prefix[:i]
            print(f"Checking subprefix: {sub_prefix}")
            if (result := prefix_cache.get(sub_prefix)) is not None:
                return result

            prefix_cache[prefix] = func(*args, **kwargs)
        return prefix_cache[prefix]

    return process_prefix
