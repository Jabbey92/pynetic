"""PyNetic Component Module"""

from collections.abc import Iterable

from .html import HTMLElement


class Component:
    """Base Component class

    Args:
        *elements (str | HTMLElement): The elements in the component

    Usage:
        ```Python
        home = Component(
            Div(
                "Hello World"
            )
        )
        ```
    """

    def __init__(self, *elements: str | HTMLElement) -> None:
        self.elements = list(elements)

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __build(self) -> ...:
        # TODO: Figure out what this is going to return. AST/CST tree or just plain text?
        pass
