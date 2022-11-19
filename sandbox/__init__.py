#!/usr/bin/env python3

from typing import Callable, TypeVar, overload

_R = TypeVar('_R')


@overload
def flip_args(
    func: Callable[[str, int], _R],
) -> Callable[[int, str], _R]:
    pass


@overload
def flip_args(
    func: Callable[[int, int], _R],
) -> Callable[[int, int], _R]:
    pass


def flip_args(func: Callable[..., _R]) -> Callable[..., _R]:
    """Contrived example, a real flip_args would use TypeVars"""

    def wrapper(p1: int, p2: str | int) -> _R:
        return func(p2, p1)

    return wrapper


def takes_string_and_int(p1: str, p2: int) -> None:
    print(f"A {p1} has {p2} vertices")


def takes_two_ints(p1: int, p2: int) -> None:
    print(f"A {p1}-sided die has {p2} vertices")


takes_string_and_int_flipped = flip_args(takes_string_and_int)
takes_two_ints_flipped = flip_args(takes_two_ints)


@overload
def takes_something_and_int(p1: str, p2: int) -> None:
    pass


@overload
def takes_something_and_int(p1: int, p2: int) -> None:
    pass


def takes_something_and_int(p1: str | int, p2: int) -> None:
    if isinstance(p1, str):
        takes_string_and_int(p1, p2)
    else:
        takes_two_ints(p1, p2)


takes_something_and_int_flipped = flip_args(takes_something_and_int)


if __name__ == '__main__':
    takes_string_and_int("cube", 8)
    takes_two_ints(20, 12)
    takes_something_and_int("cube", 8)
    takes_something_and_int(20, 12)

    takes_string_and_int_flipped(8, "cube")
    takes_two_ints_flipped(12, 20)
    takes_something_and_int_flipped(8, "cube")
    takes_something_and_int_flipped(12, 20)  # does not typecheck
