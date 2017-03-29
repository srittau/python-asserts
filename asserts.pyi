import datetime

from typing import Any, Container, Type, Callable, ContextManager


def fail(msg: str = None) -> None:
    ...


def assert_true(expr: Any, msg: str = None) -> None:
    ...


def assert_false(expr: Any, msg: str = None) -> None:
    ...


def assert_boolean_true(expr: Any, msg: str = None) -> None:
    ...


def assert_boolean_false(expr: Any, msg: str = None) -> None:
    ...


def assert_is_none(expr: Any, msg: str = None) -> None:
    ...


def assert_is_not_none(expr: Any, msg: str = None) -> None:
    ...


def assert_equal(first: Any, second: Any, msg: str = None) -> None:
    ...


def assert_not_equal(first: Any, second: Any, msg: str = None) -> None:
    ...


def assert_almost_equal(
        first: float, second: float, places: int = None, msg: str = None,
        delta: float = None) -> None:
    ...


def assert_less(first: Any, second: Any, msg: str = None) -> None:
    ...


def assert_less_equal(first: Any, second: Any, msg: str = None) -> None:
    ...


def assert_greater(first: Any, second: Any, msg: str = None) -> None:
    ...


def assert_greater_equal(first: Any, second: Any, msg: str = None) -> None:
    ...


def assert_regex(text: str, regex: str, msg: str = None) -> None:
    ...


def assert_is(first: Any, second: Any, msg: str = None) -> None:
    ...


def assert_is_not(first: Any, second: Any, msg: str = None) -> None:
    ...


def assert_in(first: Any, second: Container[Any], msg: str = None) -> None:
    ...


def assert_not_in(first: Any, second: Container[Any], msg: str = None) -> None:
    ...


def assert_between(lower_bound: Any, upper_bound: Any, expr: Any,
                   msg: str = None) -> None:
    ...


def assert_is_instance(obj: Any, cls: type, msg: str = None) -> None:
    ...


def assert_not_is_instance(obj: Any, cls: type, msg: str = None) -> None:
    ...


def assert_has_attr(obj: Any, attribute: str, msg: str = None) -> None:
    ...


_EPSILON_SECONDS = 5


def assert_datetime_about_now(actual: datetime.datetime, msg: str = None) \
        -> None:
    ...


def assert_datetime_about_now_utc(actual: datetime.datetime, msg: str = None) \
        -> None:
    ...


class AssertRaisesContext:

    def __init__(self, exception: BaseException, msg: str = None) -> None:
        ...

    def __enter__(self) -> AssertRaisesContext:
        ...

    def __exit__(self, exc_type: Type[BaseException], exc_val: BaseException,
                 exc_tb: Any) -> None:
        ...

    def add_test(self, cb: Callable[[BaseException], None]) -> None:
        ...


def assert_raises(exception: Type[BaseException], msg: str = None) \
        -> AssertRaisesContext:
    ...


def assert_raises_regex(exception: Type[BaseException], regex:  str,
                        msg: str = None) -> AssertRaisesContext:
    ...


def assert_raises_errno(exception: Type[BaseException], errno: int,
                        msg: str = None) -> AssertRaisesContext:
    ...


def assert_succeeds(exception: Type[BaseException], msg: str = None) \
        -> ContextManager:
    ...
