#!/usr/bin/env python3

from abc import ABC
from functools import wraps
from typing import Any, Callable, Generic, TypeVar, overload

_T = TypeVar('_T')


class Box(ABC, Generic[_T]):
    def __init__(self, value: _T):
        self.value = value


_P1 = TypeVar('_P1')
_P2 = TypeVar('_P2')
_P3 = TypeVar('_P3')
_R = TypeVar('_R')


@overload
def boxed_args(
    func: Callable[[_P1], _R],
) -> Callable[[Box[_P1]], _R]:
    pass


@overload
def boxed_args(
    func: Callable[[_P1, _P2], _R],
) -> Callable[[Box[_P1], Box[_P2]], _R]:
    pass


@overload
def boxed_args(
    func: Callable[[_P1, _P2, _P3], _R],
) -> Callable[[Box[_P1], Box[_P2], Box[_P3]], _R]:
    pass


def boxed_args(func: Callable[..., _R]) -> Callable[..., _R]:
    @wraps(func)
    def wrapper(*args: Any) -> _R:
        return func(*(arg.value for arg in args))

    return wrapper


def takes_str_and_default_int(p1: str, p2: int = 404) -> None:
    print(p1, p2)


@boxed_args
def takes_str_and_default_int_decorated(p1: str, p2: int = 404) -> None:
    print(p1, p2)


if __name__ == '__main__':
    # typechecks successfully
    takes_str_and_default_int("Typechecker", 1)
    # does not typecheck
    takes_str_and_default_int_decorated(Box("Luc"), Box(0))
