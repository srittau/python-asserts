"""
Rich Assertions.

This module contains several rich standard assertions that can be used in unit
tests and in implementations. Users are encouraged to define their own
assertions, possibly using assertions from this package as a basis.

    >>> assert_equal(13, 13)
    >>> assert_equal(13, 14)
    Traceback (most recent call last):
        ...
    AssertionError: 13 != 14
    >>> with assert_raises(KeyError):
    ...     raise KeyError()
    >>> with assert_raises(KeyError):
    ...     pass
    Traceback (most recent call last):
        ...
    AssertionError: KeyError not raised

"""

from datetime import datetime, timedelta
import re


def fail(msg=None):
    """Raise an AssertionError with the given message.

    >>> fail("my message")
    Traceback (most recent call last):
        ...
    AssertionError: my message

    """
    raise AssertionError(msg or "assertion failure")


def assert_true(expr, msg=None):
    """Fail the test unless the expression is truthy.

    >>> assert_true("Hello World!")
    >>> assert_true("")
    Traceback (most recent call last):
        ...
    AssertionError: '' is not truthy

    """
    if not expr:
        if not msg:
            msg = repr(expr) + " is not truthy"
        fail(msg)


def assert_false(expr, msg=None):
    """Fail the test unless the expression is falsy.

    >>> assert_false("")
    >>> assert_false("Hello World!")
    Traceback (most recent call last):
        ...
    AssertionError: 'Hello World!' is not falsy

    """
    if expr:
        if not msg:
            msg = repr(expr) + " is not falsy"
        fail(msg)


def assert_boolean_true(expr, msg=None):
    """Fail the test unless the expression is the constant True.

    >>> assert_boolean_true(True)
    >>> assert_boolean_true("Hello World!")
    Traceback (most recent call last):
        ...
    AssertionError: 'Hello World!' is not True

    """
    assert_is(expr, True, msg)


def assert_boolean_false(expr, msg=None):
    """Fail the test unless the expression is the constant False.

    >>> assert_boolean_false(False)
    >>> assert_boolean_false(0)
    Traceback (most recent call last):
        ...
    AssertionError: 0 is not False

    """
    assert_is(expr, False, msg)


def assert_is_none(expr, msg=None):
    """Fail if the expression is not None.

    >>> assert_is_none(None)
    >>> assert_is_none(False)
    Traceback (most recent call last):
        ...
    AssertionError: False is not None

    """
    assert_is(expr, None, msg)


def assert_is_not_none(expr, msg=None):
    """Fail if the expression is None.

    >>> assert_is_not_none(0)
    >>> assert_is_not_none(None)
    Traceback (most recent call last):
        ...
    AssertionError: expression is None

    """
    assert_is_not(expr, None, msg or "expression is None")


def assert_equal(first, second, msg=None):
    """Fail unless first equals second, as determined by the '==' operator.

    >>> assert_equal(5, 5.0)
    >>> assert_equal("Hello World!", "Goodbye!")
    Traceback (most recent call last):
        ...
    AssertionError: 'Hello World!' != 'Goodbye!'

    """
    if not first == second:
        fail(msg or "{!r} != {!r}".format(first, second))


def assert_not_equal(first, second, msg=None):
    """Fail if first equals second, as determined by the '==' operator.

    >>> assert_not_equal(5, 8)
    >>> assert_not_equal(-7, -7.0)
    Traceback (most recent call last):
        ...
    AssertionError: -7 == -7.0

    """
    if first == second:
        fail(msg or "{!r} == {!r}".format(first, second))


def assert_almost_equal(first, second, places=None, msg=None, delta=None):
    """Fail if first and second are not equal after rounding.

    By default, the difference between first and second is rounded to
    7 decimal places. This can be configured with the places argument.
    Alternatively, delta can be used to specify the maximum allowed
    difference between first and second.

    If first and second can not be rounded or both places and delta are
    supplied, a TypeError is raised.

    >>> assert_almost_equal(5, 5.00000001)
    >>> assert_almost_equal(5, 5.001)
    Traceback (most recent call last):
        ...
    AssertionError: 5 != 5.001 within 7 places
    >>> assert_almost_equal(5, 5.001, places=2)
    >>> assert_almost_equal(5, 5.001, delta=0.1)

    """
    if delta is not None and places is not None:
        raise TypeError("'places' and 'delta' are mutually exclusive")
    if delta is not None:
        diff = second - first
        success = diff < delta
        detail_msg = "with delta={}".format(delta)
    else:
        if places is None:
            places = 7
        success = not round(second - first, places)
        detail_msg = "within {} places".format(places)
    if not success:
        fail(msg or "{!r} != {!r} ".format(first, second) + detail_msg)


def assert_less(first, second, msg=None):
    """Fail if first is not less than second.

    >>> assert_less('bar', 'foo')
    >>> assert_less(5, 5)
    Traceback (most recent call last):
        ...
    AssertionError: 5 is not less than 5

    """
    if not first < second:
        fail(msg or "{!r} is not less than {!r}".format(first, second))


def assert_less_equal(first, second, msg=None):
    """Fail if first is not less than or equal to second.

    >>> assert_less_equal('bar', 'foo')
    >>> assert_less_equal(5, 5)
    >>> assert_less_equal(6, 5)
    Traceback (most recent call last):
        ...
    AssertionError: 6 is not less than or equal to 5

    """
    if not first <= second:
        fail(msg or "{!r} is not less than or equal to {!r}".format(
            first, second))


def assert_greater(first, second, msg=None):
    """Fail if first is not greater than second.

    >>> assert_greater('foo', 'bar')
    >>> assert_greater(5, 5)
    Traceback (most recent call last):
        ...
    AssertionError: 5 is not greater than 5

    """
    if not first > second:
        fail(msg or "{!r} is not greater than {!r}".format(first, second))


def assert_greater_equal(first, second, msg=None):
    """Fail if first is not greater than or equal to second.

    >>> assert_greater_equal('foo', 'bar')
    >>> assert_greater_equal(5, 5)
    >>> assert_greater_equal(5, 6)
    Traceback (most recent call last):
        ...
    AssertionError: 5 is not greater than or equal to 6

    """
    if not first >= second:
        fail(msg or "{!r} is not greater than or equal to {!r}".format(
            first, second))


def assert_regex(text, regex, msg=None):
    """Fail if text does not match the regular expression.

    regex can be either a regular expression string or a compiled regular
    expression object.

    >>> assert_regex("Hello World!", r"llo.*rld!$")
    >>> assert_regex("Hello World!", r"\d")
    Traceback (most recent call last):
        ...
    AssertionError: 'Hello World!' does not match '\\\\d'

    """
    compiled = re.compile(regex)
    if not compiled.search(text):
        fail(msg or "{!r} does not match {!r}".format(text, compiled.pattern))


def assert_is(first, second, msg=None):
    """Fail if first and second do not refer to the same object.

    >>> list1 = [5, "foo"]
    >>> list2 = [5, "foo"]
    >>> assert_is(list1, list1)
    >>> assert_is(list1, list2)
    Traceback (most recent call last):
        ...
    AssertionError: [5, 'foo'] is not [5, 'foo']

    """
    if first is not second:
        fail(msg or "{!r} is not {!r}".format(first, second))


def assert_is_not(first, second, msg=None):
    """Fail if first and second refer to the same object.

    >>> list1 = [5, "foo"]
    >>> list2 = [5, "foo"]
    >>> assert_is_not(list1, list2)
    >>> assert_is_not(list1, list1)
    Traceback (most recent call last):
        ...
    AssertionError: both arguments refer to [5, 'foo']

    """
    if first is second:
        fail(msg or "both arguments refer to {!r}".format(first))


def assert_in(first, second, msg=None):
    """Fail if first is not in collection second.

    >>> assert_in("foo", [4, "foo", {}])
    >>> assert_in("bar", [4, "foo", {}])
    Traceback (most recent call last):
        ...
    AssertionError: 'bar' not in [4, 'foo', {}]

    """
    msg = msg or "{!r} not in {!r}".format(first, second)
    assert_true(first in second, msg)


def assert_not_in(first, second, msg=None):
    """Fail if first is in a collection second.

    >>> assert_not_in("bar", [4, "foo", {}])
    >>> assert_not_in("foo", [4, "foo", {}])
    Traceback (most recent call last):
        ...
    AssertionError: 'foo' is in [4, 'foo', {}]

    """
    msg = msg or "{!r} is in {!r}".format(first, second)
    assert_false(first in second, msg)


def assert_between(lower_bound, upper_bound, expr, msg=None):
    """Fail if an expression is not between certain bounds (inclusive).

    >>> assert_between(5, 15, 5)
    >>> assert_between(5, 15, 15)
    >>> assert_between(5, 15, 4.9)
    Traceback (most recent call last):
        ...
    AssertionError: 4.9 is not between 5 and 15

    """
    if not lower_bound <= expr <= upper_bound:
        msg = msg or "{!r} is not between {} and {}".format(
            expr, lower_bound, upper_bound)
        fail(msg)


def assert_is_instance(obj, cls, msg=None):
    """Fail if an object is not an instance of a class or tuple of classes.

    >>> assert_is_instance(5, int)
    >>> assert_is_instance('foo', (str, bytes))
    >>> assert_is_instance(5, str)
    Traceback (most recent call last):
        ...
    AssertionError: 5 is an instance of <class 'int'>, expected <class 'str'>

    """
    if not isinstance(obj, cls):
        msg = (msg or "{!r} is an instance of {!r}, expected {!r}".format(
            obj, obj.__class__, cls))
        fail(msg)


def assert_not_is_instance(obj, cls, msg=None):
    """Fail if an object is an instance of a class or tuple of classes.

    >>> assert_not_is_instance(5, str)
    >>> assert_not_is_instance(5, (str, bytes))
    >>> assert_not_is_instance('foo', str)
    Traceback (most recent call last):
        ...
    AssertionError: 'foo' is an instance of <class 'str'>

    """
    if isinstance(obj, cls):
        msg = msg or "{!r} is an instance of {!r}".format(obj, obj.__class__)
        fail(msg)


def assert_has_attr(obj, attribute, msg=None):
    """Fail is an object does not have an attribute.

    >>> assert_has_attr([], "index")
    >>> assert_has_attr([], "i_do_not_have_this")
    Traceback (most recent call last):
        ...
    AssertionError: [] does not have attribute 'i_do_not_have_this'

    """
    if not hasattr(obj, attribute):
        fail(msg or repr(obj) + " does not have attribute '" + attribute + "'")


_EPSILON_SECONDS = 5


def assert_datetime_about_now(actual, msg=None):
    """Fail if a datetime object is not within 5 seconds of the local time.

    >>> assert_datetime_about_now(datetime.now())
    >>> assert_datetime_about_now(datetime(1900, 1, 1, 12, 0, 0))
    Traceback (most recent call last):
        ...
    AssertionError: datetime.datetime(1900, 1, 1, 12, 0) is not close to current date/time

    """
    if actual is None:
        if msg is None:
            msg = "None is not a valid date/time"
        raise AssertionError(msg)
    now = datetime.now()
    lower_bound = now - timedelta(seconds=_EPSILON_SECONDS)
    upper_bound = now + timedelta(seconds=_EPSILON_SECONDS)
    if msg is None:
        msg = "{!r} is not close to current date/time".format(actual)
    assert_between(lower_bound, upper_bound, actual, msg)


def assert_datetime_about_now_utc(actual, msg=None):
    """Fail if a datetime object is not within 5 seconds of UTC.

    >>> assert_datetime_about_now_utc(datetime.utcnow())
    >>> assert_datetime_about_now_utc(datetime(1900, 1, 1, 12, 0, 0))
    Traceback (most recent call last):
        ...
    AssertionError: datetime.datetime(1900, 1, 1, 12, 0) is not close to current UTC date/time

    """
    if actual is None:
        if msg is None:
            msg = "None is not a valid date/time"
        raise AssertionError(msg)
    now = datetime.utcnow()
    lower_bound = now - timedelta(seconds=_EPSILON_SECONDS)
    upper_bound = now + timedelta(seconds=_EPSILON_SECONDS)
    if not msg:
        msg = "{!r} is not close to current UTC date/time".format(actual)
    assert_between(lower_bound, upper_bound, actual, msg)


class AssertRaisesContext(object):

    """A context manager to test for exceptions with certain properties.

    When the context is left and no exception has been raised, an
    AssertionError will be raised:

        >>> context = AssertRaisesContext(TypeError)
        >>> with context:
        ...    pass
        Traceback (most recent call last):
            ...
        AssertionError: TypeError not raised

    If an exception that is not a sub-class of the exception class provided
    to the constructor is raised, it will be passed on:

        >>> with context:
        ...    raise ValueError("Wrong Class")
        Traceback (most recent call last):
            ...
        ValueError: Wrong Class

    If the exception has the right class, any additional tests that have been
    configured on the context, will be called:

        >>> def test(exc):
        ...     assert_equal("Hello World!", str(exc))
        >>> context.add_test(test)
        >>> with context:
        ...     raise TypeError("Wrong Message")
        Traceback (most recent call last):
            ...
        AssertionError: 'Hello World!' != 'Wrong Message'

    """

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
        class was raised. The callback will get the raised exception as only
        argument.

        """
        self._tests.append(cb)


def assert_raises(exception, msg=None):
    """Fail unless a specific exception is raised inside the context.

    If a different type of exception is raised, it will not be caught.

    >>> with assert_raises(TypeError):
    ...     raise TypeError()
    ...
    >>> with assert_raises(TypeError):
    ...     pass
    ...
    Traceback (most recent call last):
        ...
    AssertionError: TypeError not raised
    >>> with assert_raises(TypeError):
    ...     raise ValueError("wrong error")
    ...
    Traceback (most recent call last):
        ...
    ValueError: wrong error

    """
    return AssertRaisesContext(exception, msg)


def assert_raises_regex(exception, regex, msg=None):
    """Fail unless an exception with a message that matches a regular
     expression is raised within the context.

    The regular expression can be a regular expression string or object.

    >>> with assert_raises_regex(ValueError, r"\d+"):
    ...     raise ValueError("Error #42")
    ...
    >>> with assert_raises_regex(ValueError, r"\d+"):
    ...     raise ValueError("Generic Error")
    ...
    Traceback (most recent call last):
        ...
    AssertionError: 'Generic Error' does not match '\\\\d+'

    """

    def test(exc):
        assert_regex(str(exc), regex, msg)

    context = AssertRaisesContext(exception, msg)
    context.add_test(test)
    return context


def assert_raises_errno(exception, errno, msg=None):
    """Fail unless an exception with a specific errno is raised with the
     context.

    >>> with assert_raises_errno(OSError, 42):
    ...     raise OSError(42, "OS Error")
    ...
    >>> with assert_raises_errno(OSError, 44):
    ...     raise OSError(17, "OS Error")
    ...
    Traceback (most recent call last):
        ...
    AssertionError: wrong errno: 44 != 17

    """

    def check_errno(exc):
        if errno != exc.errno:
            fail(msg or "wrong errno: {!r} != {!r}".format(errno, exc.errno))
    context = AssertRaisesContext(exception, msg)
    context.add_test(check_errno)
    return context


def assert_succeeds(exception, msg=None):
    """Fail if a specific exception is raised within the context.

    This assertion should be used for cases, where successfully running a
    function signals a successful test, and raising the exception of a
    certain type signals a test failure. All other raised exceptions are
    passed on and will usually still result in a test error. This can be
    used to signal the intent of a block.

    >>> l = ["foo", "bar"]
    >>> with assert_succeeds(ValueError):
    ...     i = l.index("foo")
    ...
    >>> with assert_succeeds(ValueError):
    ...     raise ValueError()
    ...
    Traceback (most recent call last):
        ...
    AssertionError: ValueError was unexpectedly raised
    >>> with assert_succeeds(ValueError):
    ...     raise TypeError("Wrong Error")
    ...
    Traceback (most recent call last):
        ...
    TypeError: Wrong Error

    """

    class _AssertSucceeds(object):

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type and issubclass(exc_type, exception):
                fail(msg or exception.__name__ + " was unexpectedly raised")

    return _AssertSucceeds()
