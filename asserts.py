"""
Rich Assertions.

This module contains several rich standard assertions that can be used in unit
tests and in implementations. Users are encouraged to define their own
assertions, possibly using assertions from this package as a basis.

"""

from datetime import datetime, timedelta
import re


def fail(msg=None):
    """Raise an AssertionError with the given message."""
    raise AssertionError(msg or "assertion failure")


def assert_true(expr, msg=None):
    """Fail the test unless the expression is truthy."""
    if not expr:
        if not msg:
            msg = repr(expr) + " is not true"
        fail(msg)


def assert_false(expr, msg=None):
    """Fail the test unless the expression is falsy."""
    if expr:
        if not msg:
            msg = repr(expr) + " is not false"
        fail(msg)


def assert_boolean_true(expr, msg=None):
    """Fail the test unless the expression is the constant True."""
    assert_is(True, expr, msg)


def assert_boolean_false(expr, msg=None):
    """Fail the test unless the expression is the constant False."""
    assert_is(False, expr, msg)


def assert_is_none(expr, msg=None):
    """Fail if actual is not None."""
    if expr is not None:
        fail(msg or "{!r} is not None".format(expr))


def assert_is_not_none(expr, msg=None):
    """Fail if actual is None."""
    if expr is None:
        fail(msg or "{!r} is None".format(expr))


def assert_equal(first, second, msg=None):
    """Fail if actual does not equal expected, as determined by the '=='
    operator.

    """
    if not first == second:
        fail(msg or "{!r} != {!r}".format(first, second))


def assert_not_equal(first, second, msg=None):
    """Fail if the two objects are equal as determined by the '=='
    operator.

    """
    if first == second:
        fail(msg or "{!r} == {!r}".format(first, second))


def assert_almost_equal(first, second, places=7, msg=None):
    """Fail if the two objects are unequal when rounded."""
    if round(second - first, places):
        fail(msg or "{!r} != {!r} within {} places".format(first, second,
                                                           places))


def assert_regex(text, regex, msg=None):
    """Fail if actual does not match the regular expression expected."""
    compiled = re.compile(regex)
    if not compiled.search(text):
        fail(msg or "{!r} does not match {!r}".format(text, compiled.pattern))


def assert_is(first, second, msg=None):
    """Fail if the two objects are not the same object."""
    if first is not second:
        fail(msg or "{!r} is not {!r}".format(first, second))


def assert_is_not(first, second, msg=None):
    """Fail if the two objects are the same object."""
    if first is second:
        fail(msg or "{!r} is {!r}".format(first, second))


def assert_in(first, second, msg=None):
    """Fail if an element is not in a collection."""
    msg = msg or "{!r} not in {!r}".format(first, second)
    assert_true(first in second, msg)


def assert_not_in(first, second, msg=None):
    """Fail if an element is in a collection."""
    msg = msg or "{!r} is in {!r}".format(first, second)
    assert_false(first in second, msg)


def assert_between(lower_bound, upper_bound, actual, msg=None):
    if not lower_bound <= actual <= upper_bound:
        msg = msg or "{!r} is not between {} and {}".format(
            actual, lower_bound, upper_bound)
        fail(msg)


def assert_is_instance(obj, cls, msg=None):
    if not isinstance(obj, cls):
        msg = (msg if msg is not None else
               repr(obj) + " is of " + repr(obj.__class__) +
               " not of " + repr(cls))
        fail(msg)


def assert_has_attr(obj, attribute, msg=None):
    if not hasattr(obj, attribute):
        fail(msg or repr(obj) + " is missing attribute '" + attribute + "'")


_EPSILON_SECONDS = 5


def assert_datetime_about_now(actual, msg=None):
    now = datetime.now()
    lower_bound = now - timedelta(seconds=_EPSILON_SECONDS)
    upper_bound = now + timedelta(seconds=_EPSILON_SECONDS)
    if not msg:
        msg = repr(actual) + " is not close to current " + repr(now)
    assert_between(lower_bound, upper_bound, actual, msg)


def assert_datetime_about_now_utc(actual, msg=None):
    now = datetime.utcnow()
    lower_bound = now - timedelta(seconds=_EPSILON_SECONDS)
    upper_bound = now + timedelta(seconds=_EPSILON_SECONDS)
    if not msg:
        msg = repr(actual) + " is not close to current UTC " + repr(now)
    assert_between(lower_bound, upper_bound, actual, msg)


class AssertRaisesContext(object):

    def __init__(self, exception, msg=None):
        self.exception = exception
        self.msg = msg
        self._exception_name = getattr(exception, "__name__", str(exception))
        self._tests = []

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            fail(self.msg or "{} not raised".format(self._exception_name))
        if not issubclass(exc_type, self.exception):
            return False
        for test in self._tests:
            test(exc_val)
        return True

    def add_test(self, cb):
        """Add a test callback.

        This callback is called after determining that the right exception
        class was raised.

        """
        self._tests.append(cb)


def assert_raises(exception, msg=None):
    """Fail unless a specific exception is raised inside the context.

    If a different type of exception is raised, it will not be caught.

    """
    return AssertRaisesContext(exception, msg)


def assert_raises_regex(exception, regex, msg=None):
    """Like assert_raises, but also ensures that the exception message
    matches a regular expression.

    The regular expression can be a regular expression string or object.

    """

    def test(exc):
        assert_regex(str(exc), regex, msg)

    context = AssertRaisesContext(exception, msg)
    context.add_test(test)
    return context


def assert_raises_errno(exception, errno, msg=None):
    """Fail unless the context raises an exception of class exc_cls and
    its errno attribute equals the supplied one.

    """

    def check_errno(exc):
        assert_equal(errno, exc.errno, msg)
    context = AssertRaisesContext(exception, msg)
    context.add_test(check_errno)
    return context


def assert_succeeds(exception, msg=None):
    """Fail if an exception of the provided type is raised within the context.

    This assertion should be used for cases, where successfully running a
    function signals a successful test, and raising the exception of a
    certain type signals a test failure. All other raised exceptions are
    passed on and will usually still result in a test error. This can be
    used to signal intent of a function call.

    >>> l = ["foo", "bar"]
    >>> with assert_succeeds(ValueError):
    ...     l.index("foo")
    ...
    >>> def raise_value_error():
    ...     raise ValueError()
    ...
    >>> with assert_succeeds(ValueError):
    ...     raise ValueError()
    ...
    Traceback (most recent call last):
    ...
    AssertionError: ValueError was raised during the execution of raise_value_error

    """

    class _AssertSucceeds(object):

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type and issubclass(exc_type, exception):
                fail(msg or exception.__name__ + " was unexpectedly raised")

    return _AssertSucceeds()
