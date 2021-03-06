"""pynetic utilities module"""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from itertools import count, product
from string import ascii_lowercase, ascii_uppercase
from types import FunctionType
from typing import Any, TypeVar

all_letters = ascii_lowercase + ascii_uppercase


class For:
    """Replacement for builtin for loop to use inline with DOM elements

    Args:
        each (Iterable): The iterable to loop over
        condition (Callable | None): The function to use as a condition in the for loop
        do (Callable): What to do in the loop

    Usage:
        ```Python
        my_list = ["Button 1", "Button 2", "Button 3"]
        Div(
            For(
                my_list,
                lambda x: x != 2,
                lambda name: Button(name)
            )

        )
    """

    def __init__(self, each: Iterable, condition: Callable | None, statements: Any, /) -> None:
        self.each = each
        self.condition = condition
        self.statements = statements


def iter_short_names():
    """Generator over a-z ... A-Z ... aa-ZZ ..."""
    for i in count():
        yield from map("".join, product(all_letters, repeat=i))
