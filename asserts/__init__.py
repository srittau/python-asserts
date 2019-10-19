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

import re
import sys
from datetime import datetime, timedelta
from json import loads as json_loads
from warnings import catch_warnings


def fail(msg=None):
    """Raise an AssertionError with the given message.

    >>> fail("my message")
    Traceback (most recent call last):
        ...
    AssertionError: my message

    """
    raise AssertionError(msg or "assertion failure")


def assert_true(expr, msg_fmt="{msg}"):
    """Fail the test unless the expression is truthy.

    >>> assert_true("Hello World!")
    >>> assert_true("")
    Traceback (most recent call last):
        ...
    AssertionError: '' is not truthy

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * expr - tested expression
    """

    if not expr:
        msg = "{!r} is not truthy".format(expr)
        fail(msg_fmt.format(msg=msg, expr=expr))


def assert_false(expr, msg_fmt="{msg}"):
    """Fail the test unless the expression is falsy.

    >>> assert_false("")
    >>> assert_false("Hello World!")
    Traceback (most recent call last):
        ...
    AssertionError: 'Hello World!' is not falsy

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * expr - tested expression
    """

    if expr:
        msg = "{!r} is not falsy".format(expr)
        fail(msg_fmt.format(msg=msg, expr=expr))


def assert_boolean_true(expr, msg_fmt="{msg}"):
    """Fail the test unless the expression is the constant True.

    >>> assert_boolean_true(True)
    >>> assert_boolean_true("Hello World!")
    Traceback (most recent call last):
        ...
    AssertionError: 'Hello World!' is not True

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * expr - tested expression
    """

    if expr is not True:
        msg = "{!r} is not True".format(expr)
        fail(msg_fmt.format(msg=msg, expr=expr))


def assert_boolean_false(expr, msg_fmt="{msg}"):
    """Fail the test unless the expression is the constant False.

    >>> assert_boolean_false(False)
    >>> assert_boolean_false(0)
    Traceback (most recent call last):
        ...
    AssertionError: 0 is not False

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * expr - tested expression
    """

    if expr is not False:
        msg = "{!r} is not False".format(expr)
        fail(msg_fmt.format(msg=msg, expr=expr))


def assert_is_none(expr, msg_fmt="{msg}"):
    """Fail if the expression is not None.

    >>> assert_is_none(None)
    >>> assert_is_none(False)
    Traceback (most recent call last):
        ...
    AssertionError: False is not None

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * expr - tested expression
    """

    if expr is not None:
        msg = "{!r} is not None".format(expr)
        fail(msg_fmt.format(msg=msg, expr=expr))


def assert_is_not_none(expr, msg_fmt="{msg}"):
    """Fail if the expression is None.

    >>> assert_is_not_none(0)
    >>> assert_is_not_none(None)
    Traceback (most recent call last):
        ...
    AssertionError: expression is None

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * expr - tested expression
    """
    if expr is None:
        msg = "expression is None"
        fail(msg_fmt.format(msg=msg, expr=expr))


def assert_equal(first, second, msg_fmt="{msg}"):
    """Fail unless first equals second, as determined by the '==' operator.

    >>> assert_equal(5, 5.0)
    >>> assert_equal("Hello World!", "Goodbye!")
    Traceback (most recent call last):
        ...
    AssertionError: 'Hello World!' != 'Goodbye!'

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    """

    if isinstance(first, dict) and isinstance(second, dict):
        assert_dict_equal(first, second, msg_fmt)
    elif not first == second:
        msg = "{!r} != {!r}".format(first, second)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_not_equal(first, second, msg_fmt="{msg}"):
    """Fail if first equals second, as determined by the '==' operator.

    >>> assert_not_equal(5, 8)
    >>> assert_not_equal(-7, -7.0)
    Traceback (most recent call last):
        ...
    AssertionError: -7 == -7.0

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    """

    if first == second:
        msg = "{!r} == {!r}".format(first, second)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_almost_equal(
    first, second, msg_fmt="{msg}", places=None, delta=None
):
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

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    * places - number of places to compare or None
    * delta - delta or None
    """

    if delta is not None and places is not None:
        raise TypeError("'places' and 'delta' are mutually exclusive")
    if delta is not None:
        if delta <= 0:
            raise ValueError("delta must be larger than 0")
        diff = abs(second - first)
        success = diff < delta
        detail_msg = "with delta={}".format(delta)
    else:
        if places is None:
            places = 7
        success = not round(second - first, places)
        detail_msg = "within {} places".format(places)
    if not success:
        msg = "{!r} != {!r} {}".format(first, second, detail_msg)
        fail(
            msg_fmt.format(
                msg=msg, first=first, second=second, places=places, delta=delta
            )
        )


def assert_not_almost_equal(
    first, second, msg_fmt="{msg}", places=None, delta=None
):
    """Fail if first and second are equal after rounding.

    By default, the difference between first and second is rounded to
    7 decimal places. This can be configured with the places argument.
    Alternatively, delta can be used to specify the maximum allowed
    difference between first and second.

    If first and second can not be rounded or both places and delta are
    supplied, a TypeError is raised.

    >>> assert_not_almost_equal(5, 5.001)
    >>> assert_not_almost_equal(5, 5.00000001)
    Traceback (most recent call last):
        ...
    AssertionError: 5 == 5.00000001 within 7 places
    >>> assert_not_almost_equal(5, 5.001, places=2)
    Traceback (most recent call last):
        ...
    AssertionError: 5 == 5.001 within 2 places
    >>> assert_not_almost_equal(5, 5.001, delta=0.1)
    Traceback (most recent call last):
        ...
    AssertionError: 5 == 5.001 with delta=0.1

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    * places - number of places to compare or None
    * delta - delta or None
    """

    if delta is not None and places is not None:
        raise TypeError("'places' and 'delta' are mutually exclusive")
    if delta is not None:
        if delta <= 0:
            raise ValueError("delta must be larger than 0")
        diff = abs(second - first)
        success = diff >= delta
        detail_msg = "with delta={}".format(delta)
    else:
        if places is None:
            places = 7
        success = bool(round(second - first, places))
        detail_msg = "within {} places".format(places)
    if not success:
        msg = "{!r} == {!r} {}".format(first, second, detail_msg)
        fail(
            msg_fmt.format(
                msg=msg, first=first, second=second, places=places, delta=delta
            )
        )


def assert_dict_equal(
    first, second, key_msg_fmt="{msg}", value_msg_fmt="{msg}"
):
    """Fail unless first dictionary equals second.

    The dictionaries are considered equal, if they both contain the same
    keys, and their respective values are also equal.

    >>> assert_dict_equal({"foo": 5}, {"foo": 5})
    >>> assert_dict_equal({"foo": 5}, {})
    Traceback (most recent call last):
        ...
    AssertionError: key 'foo' missing from right dict

    The following key_msg_fmt arguments are supported, if the keys do not
    match:
    * msg - the default error message
    * first - the first dict
    * second - the second dict
    * missing_keys - list of keys missing from right
    * extra_keys - list of keys missing from left

    The following value_msg_fmt arguments are supported, if a value does not
    match:
    * msg - the default error message
    * first - the first dict
    * second - the second dict
    * key - the key where the value does not match
    * first_value - the value in the first dict
    * second_value - the value in the second dict
    """
    first_keys = set(first.keys())
    second_keys = set(second.keys())
    missing_keys = list(first_keys - second_keys)
    extra_keys = list(second_keys - first_keys)
    if missing_keys or extra_keys:
        if missing_keys:
            if len(missing_keys) == 1:
                msg = "key {!r} missing from right dict".format(
                    missing_keys[0]
                )
            else:
                keys = ", ".join(sorted(repr(k) for k in missing_keys))
                msg = "keys {} missing from right dict".format(keys)
        else:
            if len(extra_keys) == 1:
                msg = "extra key {!r} in right dict".format(extra_keys[0])
            else:
                keys = ", ".join(sorted(repr(k) for k in extra_keys))
                msg = "extra keys {} in right dict".format(keys)
        if key_msg_fmt:
            msg = key_msg_fmt.format(
                msg=msg,
                first=first,
                second=second,
                missing_keys=missing_keys,
                extra_keys=extra_keys,
            )
        raise AssertionError(msg)
    for key in first:
        first_value = first[key]
        second_value = second[key]
        msg = "key '{}' differs: {!r} != {!r}".format(
            key, first_value, second_value
        )
        if value_msg_fmt:
            msg = value_msg_fmt.format(
                msg=msg,
                first=first,
                second=second,
                key=key,
                first_value=first_value,
                second_value=second_value,
            )
        msg = msg.replace("{", "{{").replace("}", "}}")
        assert_equal(first_value, second_value, msg_fmt=msg)


def assert_dict_superset(
    first, second, key_msg_fmt="{msg}", value_msg_fmt="{msg}"
):
    """Fail unless second dictionary is a superset of the first.

    The second dictionary must contain all keys of the first and their
    values are equal (or a superset in case of dicts). But the second
    dictionary can contain additional keys.

    >>> assert_dict_superset({"foo": 5}, {"foo": 5, "bar": 10})
    >>> assert_dict_superset({"foo": 5}, {})
    Traceback (most recent call last):
        ...
    AssertionError: key 'foo' missing from right dict

    The following key_msg_fmt arguments are supported, if the keys do not
    match:
    * msg - the default error message
    * first - the first dict
    * second - the second dict
    * missing_keys - list of keys missing from right

    The following value_msg_fmt arguments are supported, if a value does not
    match:
    * msg - the default error message
    * first - the first dict
    * second - the second dict
    * key - the key where the value does not match
    * first_value - the value in the first dict
    * second_value - the value in the second dict
    """
    first_keys = set(first.keys())
    second_keys = set(second.keys())
    missing_keys = list(first_keys - second_keys)
    if missing_keys:
        if len(missing_keys) == 1:
            msg = "key {!r} missing from right dict".format(missing_keys[0])
        else:
            keys = ", ".join(sorted(repr(k) for k in missing_keys))
            msg = "keys {} missing from right dict".format(keys)
        if key_msg_fmt:
            msg = key_msg_fmt.format(
                msg=msg, first=first, second=second, missing_keys=missing_keys
            )
        raise AssertionError(msg)
    for key in first:
        first_value = first[key]
        second_value = second[key]
        msg = "key '{}' differs: {!r} != {!r}".format(
            key, first_value, second_value
        )
        if value_msg_fmt:
            msg = value_msg_fmt.format(
                msg=msg,
                first=first,
                second=second,
                key=key,
                first_value=first_value,
                second_value=second_value,
            )
        msg = msg.replace("{", "{{").replace("}", "}}")
        assert_equal(first_value, second_value, msg_fmt=msg)


def assert_less(first, second, msg_fmt="{msg}"):
    """Fail if first is not less than second.

    >>> assert_less('bar', 'foo')
    >>> assert_less(5, 5)
    Traceback (most recent call last):
        ...
    AssertionError: 5 is not less than 5

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    """

    if not first < second:
        msg = "{!r} is not less than {!r}".format(first, second)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_less_equal(first, second, msg_fmt="{msg}"):
    """Fail if first is not less than or equal to second.

    >>> assert_less_equal('bar', 'foo')
    >>> assert_less_equal(5, 5)
    >>> assert_less_equal(6, 5)
    Traceback (most recent call last):
        ...
    AssertionError: 6 is not less than or equal to 5

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    """

    if not first <= second:
        msg = "{!r} is not less than or equal to {!r}".format(first, second)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_greater(first, second, msg_fmt="{msg}"):
    """Fail if first is not greater than second.

    >>> assert_greater('foo', 'bar')
    >>> assert_greater(5, 5)
    Traceback (most recent call last):
        ...
    AssertionError: 5 is not greater than 5

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    """

    if not first > second:
        msg = "{!r} is not greater than {!r}".format(first, second)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_greater_equal(first, second, msg_fmt="{msg}"):
    """Fail if first is not greater than or equal to second.

    >>> assert_greater_equal('foo', 'bar')
    >>> assert_greater_equal(5, 5)
    >>> assert_greater_equal(5, 6)
    Traceback (most recent call last):
        ...
    AssertionError: 5 is not greater than or equal to 6

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    """

    if not first >= second:
        msg = "{!r} is not greater than or equal to {!r}".format(first, second)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_regex(text, regex, msg_fmt="{msg}"):
    """Fail if text does not match the regular expression.

    regex can be either a regular expression string or a compiled regular
    expression object.

    >>> assert_regex("Hello World!", r"llo.*rld!$")
    >>> assert_regex("Hello World!", r"\\d")
    Traceback (most recent call last):
        ...
    AssertionError: 'Hello World!' does not match '\\\\d'

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * text - text that is matched
    * pattern - regular expression pattern as string
    """

    compiled = re.compile(regex)
    if not compiled.search(text):
        msg = "{!r} does not match {!r}".format(text, compiled.pattern)
        fail(msg_fmt.format(msg=msg, text=text, pattern=compiled.pattern))


def assert_is(first, second, msg_fmt="{msg}"):
    """Fail if first and second do not refer to the same object.

    >>> list1 = [5, "foo"]
    >>> list2 = [5, "foo"]
    >>> assert_is(list1, list1)
    >>> assert_is(list1, list2)
    Traceback (most recent call last):
        ...
    AssertionError: [5, 'foo'] is not [5, 'foo']

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    """

    if first is not second:
        msg = "{!r} is not {!r}".format(first, second)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_is_not(first, second, msg_fmt="{msg}"):
    """Fail if first and second refer to the same object.

    >>> list1 = [5, "foo"]
    >>> list2 = [5, "foo"]
    >>> assert_is_not(list1, list2)
    >>> assert_is_not(list1, list1)
    Traceback (most recent call last):
        ...
    AssertionError: both arguments refer to [5, 'foo']

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the first argument
    * second - the second argument
    """

    if first is second:
        msg = "both arguments refer to {!r}".format(first)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_in(first, second, msg_fmt="{msg}"):
    """Fail if first is not in collection second.

    >>> assert_in("foo", [4, "foo", {}])
    >>> assert_in("bar", [4, "foo", {}])
    Traceback (most recent call last):
        ...
    AssertionError: 'bar' not in [4, 'foo', {}]

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the element looked for
    * second - the container looked in
    """

    if first not in second:
        msg = "{!r} not in {!r}".format(first, second)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_not_in(first, second, msg_fmt="{msg}"):
    """Fail if first is in a collection second.

    >>> assert_not_in("bar", [4, "foo", {}])
    >>> assert_not_in("foo", [4, "foo", {}])
    Traceback (most recent call last):
        ...
    AssertionError: 'foo' is in [4, 'foo', {}]

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - the element looked for
    * second - the container looked in
    """
    if first in second:
        msg = "{!r} is in {!r}".format(first, second)
        fail(msg_fmt.format(msg=msg, first=first, second=second))


def assert_count_equal(sequence1, sequence2, msg_fmt="{msg}"):
    """Compare the items of two sequences, ignoring order.

    >>> assert_count_equal([1, 2], {2, 1})

    Items missing in either sequence will be listed:

    >>> assert_count_equal(["a", "b", "c"], ["a", "d"])
    Traceback (most recent call last):
        ...
    AssertionError: missing from sequence 1: 'd'; missing from sequence 2: 'b', 'c'

    Items are counted in each sequence. This makes it useful to detect
    duplicates:

    >>> assert_count_equal({"a", "b"}, ["a", "a", "b"])
    Traceback (most recent call last):
        ...
    AssertionError: missing from sequence 1: 'a'

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * first - first sequence
    * second - second sequence
    """

    def compare():
        missing1 = list(sequence2)
        missing2 = []
        for item in sequence1:
            try:
                missing1.remove(item)
            except ValueError:
                missing2.append(item)
        return missing1, missing2

    def build_message():
        msg = ""
        if missing_from_1:
            msg += "missing from sequence 1: " + ", ".join(
                repr(i) for i in missing_from_1
            )
        if missing_from_1 and missing_from_2:
            msg += "; "
        if missing_from_2:
            msg += "missing from sequence 2: " + ", ".join(
                repr(i) for i in missing_from_2
            )
        return msg

    missing_from_1, missing_from_2 = compare()
    if missing_from_1 or missing_from_2:
        fail(
            msg_fmt.format(
                msg=build_message(), first=sequence1, second=sequence2
            )
        )


def assert_between(lower_bound, upper_bound, expr, msg_fmt="{msg}"):
    """Fail if an expression is not between certain bounds (inclusive).

    >>> assert_between(5, 15, 5)
    >>> assert_between(5, 15, 15)
    >>> assert_between(5, 15, 4.9)
    Traceback (most recent call last):
        ...
    AssertionError: 4.9 is not between 5 and 15

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * lower - lower bound
    * upper - upper bound
    * expr - tested expression
    """

    if not lower_bound <= expr <= upper_bound:
        msg = "{!r} is not between {} and {}".format(
            expr, lower_bound, upper_bound
        )
        fail(
            msg_fmt.format(
                msg=msg, lower=lower_bound, upper=upper_bound, expr=expr
            )
        )


def assert_is_instance(obj, cls, msg_fmt="{msg}"):
    """Fail if an object is not an instance of a class or tuple of classes.

    >>> assert_is_instance(5, int)
    >>> assert_is_instance('foo', (str, bytes))
    >>> assert_is_instance(5, str)
    Traceback (most recent call last):
        ...
    AssertionError: 5 is an instance of <class 'int'>, expected <class 'str'>

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * obj - object to test
    * types - tuple of types tested against
    """
    if not isinstance(obj, cls):
        msg = "{!r} is an instance of {!r}, expected {!r}".format(
            obj, obj.__class__, cls
        )
        types = cls if isinstance(cls, tuple) else (cls,)
        fail(msg_fmt.format(msg=msg, obj=obj, types=types))


def assert_not_is_instance(obj, cls, msg_fmt="{msg}"):
    """Fail if an object is an instance of a class or tuple of classes.

    >>> assert_not_is_instance(5, str)
    >>> assert_not_is_instance(5, (str, bytes))
    >>> assert_not_is_instance('foo', str)
    Traceback (most recent call last):
        ...
    AssertionError: 'foo' is an instance of <class 'str'>

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * obj - object to test
    * types - tuple of types tested against
    """
    if isinstance(obj, cls):
        msg = "{!r} is an instance of {!r}".format(obj, obj.__class__)
        types = cls if isinstance(cls, tuple) else (cls,)
        fail(msg_fmt.format(msg=msg, obj=obj, types=types))


def assert_has_attr(obj, attribute, msg_fmt="{msg}"):
    """Fail is an object does not have an attribute.

    >>> assert_has_attr([], "index")
    >>> assert_has_attr([], "i_do_not_have_this")
    Traceback (most recent call last):
        ...
    AssertionError: [] does not have attribute 'i_do_not_have_this'

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * obj - object to test
    * attribute - name of the attribute to check
    """

    if not hasattr(obj, attribute):
        msg = "{!r} does not have attribute '{}'".format(obj, attribute)
        fail(msg_fmt.format(msg=msg, obj=obj, attribute=attribute))


_EPSILON_SECONDS = 5


def assert_datetime_about_now(actual, msg_fmt="{msg}"):
    """Fail if a datetime object is not within 5 seconds of the local time.

    >>> assert_datetime_about_now(datetime.now())
    >>> assert_datetime_about_now(datetime(1900, 1, 1, 12, 0, 0))
    Traceback (most recent call last):
        ...
    AssertionError: datetime.datetime(1900, 1, 1, 12, 0) is not close to current date/time

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * actual - datetime object to check
    * now - current datetime that was tested against
    """

    now = datetime.now()
    if actual is None:
        msg = "None is not a valid date/time"
        fail(msg_fmt.format(msg=msg, actual=actual, now=now))
    lower_bound = now - timedelta(seconds=_EPSILON_SECONDS)
    upper_bound = now + timedelta(seconds=_EPSILON_SECONDS)
    if not lower_bound <= actual <= upper_bound:
        msg = "{!r} is not close to current date/time".format(actual)
        fail(msg_fmt.format(msg=msg, actual=actual, now=now))


def assert_datetime_about_now_utc(actual, msg_fmt="{msg}"):
    """Fail if a datetime object is not within 5 seconds of UTC.

    >>> assert_datetime_about_now_utc(datetime.utcnow())
    >>> assert_datetime_about_now_utc(datetime(1900, 1, 1, 12, 0, 0))
    Traceback (most recent call last):
        ...
    AssertionError: datetime.datetime(1900, 1, 1, 12, 0) is not close to current UTC date/time

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * actual - datetime object to check
    * now - current datetime that was tested against
    """

    now = datetime.utcnow()
    if actual is None:
        msg = "None is not a valid date/time"
        fail(msg_fmt.format(msg=msg, actual=actual, now=now))
    lower_bound = now - timedelta(seconds=_EPSILON_SECONDS)
    upper_bound = now + timedelta(seconds=_EPSILON_SECONDS)
    if not lower_bound <= actual <= upper_bound:
        msg = "{!r} is not close to current UTC date/time".format(actual)
        fail(msg_fmt.format(msg=msg, actual=actual, now=now))


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

    def __init__(self, exception, msg_fmt="{msg}"):
        self.exception = exception
        self.msg_fmt = msg_fmt
        self._exc_type = exception
        self._exc_val = None
        self._exception_name = getattr(exception, "__name__", str(exception))
        self._tests = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type or not exc_val:
            msg = "{} not raised".format(self._exception_name)
            fail(self.format_message(msg))
        self._exc_val = exc_val
        if not issubclass(exc_type, self.exception):
            return False
        for test in self._tests:
            test(exc_val)
        return True

    def format_message(self, default_msg):
        return self.msg_fmt.format(
            msg=default_msg,
            exc_type=self._exc_type,
            exc_name=self._exception_name,
        )

    def add_test(self, cb):
        """Add a test callback.

        This callback is called after determining that the right exception
        class was raised. The callback will get the raised exception as only
        argument.

        """
        self._tests.append(cb)

    @property
    def exc_val(self):
        if self._exc_val is None:
            raise RuntimeError("must be called after leaving the context")
        return self._exc_val


class AssertRaisesRegexContext(AssertRaisesContext):

    """A context manager to test for exceptions and their messages."""

    def __init__(self, exception, pattern, msg_fmt="{msg}"):
        super(AssertRaisesRegexContext, self).__init__(exception, msg_fmt)
        self.pattern = pattern

    def format_message(self, default_msg):
        return self.msg_fmt.format(
            msg=default_msg,
            exc_type=self._exc_type,
            exc_name=self._exception_name,
            pattern=self.pattern,
            text="",
        )


class AssertRaisesErrnoContext(AssertRaisesContext):

    """A context manager to test for exceptions with errnos."""

    def __init__(self, exception, expected_errno, msg_fmt="{msg}"):
        super(AssertRaisesErrnoContext, self).__init__(exception, msg_fmt)
        self.expected_errno = expected_errno

    def format_message(self, default_msg):
        return self.msg_fmt.format(
            msg=default_msg,
            exc_type=self._exc_type,
            exc_name=self._exception_name,
            expected_errno=self.expected_errno,
            actual_errno=None,
        )


def assert_raises(exception, msg_fmt="{msg}"):
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

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * exc_type - exception type that is expected
    * exc_name - expected exception type name
    """

    return AssertRaisesContext(exception, msg_fmt)


def assert_raises_regex(exception, regex, msg_fmt="{msg}"):
    """Fail unless an exception with a message that matches a regular
     expression is raised within the context.

    The regular expression can be a regular expression string or object.

    >>> with assert_raises_regex(ValueError, r"\\d+"):
    ...     raise ValueError("Error #42")
    ...
    >>> with assert_raises_regex(ValueError, r"\\d+"):
    ...     raise ValueError("Generic Error")
    ...
    Traceback (most recent call last):
        ...
    AssertionError: 'Generic Error' does not match '\\\\d+'

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * exc_type - exception type that is expected
    * exc_name - expected exception type name
    * text - actual error text
    * pattern - expected error message as regular expression string
    """

    def test(exc):
        compiled = re.compile(regex)
        if not exc.args:
            msg = "{} without message".format(exception.__name__)
            fail(
                msg_fmt.format(
                    msg=msg,
                    text=None,
                    pattern=compiled.pattern,
                    exc_type=exception,
                    exc_name=exception.__name__,
                )
            )
        text = exc.args[0]
        if not compiled.search(text):
            msg = "{!r} does not match {!r}".format(text, compiled.pattern)
            fail(
                msg_fmt.format(
                    msg=msg,
                    text=text,
                    pattern=compiled.pattern,
                    exc_type=exception,
                    exc_name=exception.__name__,
                )
            )

    context = AssertRaisesRegexContext(exception, regex, msg_fmt)
    context.add_test(test)
    return context


def assert_raises_errno(exception, errno, msg_fmt="{msg}"):
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

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * exc_type - exception type that is expected
    * exc_name - expected exception type name
    * expected_errno -
    * actual_errno - raised errno or None if no matching exception was raised
    """

    def check_errno(exc):
        if errno != exc.errno:
            msg = "wrong errno: {!r} != {!r}".format(errno, exc.errno)
            fail(
                msg_fmt.format(
                    msg=msg,
                    exc_type=exception,
                    exc_name=exception.__name__,
                    expected_errno=errno,
                    actual_errno=exc.errno,
                )
            )

    context = AssertRaisesErrnoContext(exception, errno, msg_fmt)
    context.add_test(check_errno)
    return context


def assert_succeeds(exception, msg_fmt="{msg}"):
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

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * exc_type - exception type
    * exc_name - exception type name
    * exception - exception that was raised
    """

    class _AssertSucceeds(object):
        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type and issubclass(exc_type, exception):
                msg = exception.__name__ + " was unexpectedly raised"
                fail(
                    msg_fmt.format(
                        msg=msg,
                        exc_type=exception,
                        exc_name=exception.__name__,
                        exception=exc_val,
                    )
                )

    return _AssertSucceeds()


class AssertWarnsContext(object):

    """A context manager to test for warnings with certain properties.

    When the context is left and the expected warning has not been raised, an
    AssertionError will be raised:

        >>> context = AssertWarnsContext(DeprecationWarning)
        >>> with context:
        ...    pass
        Traceback (most recent call last):
            ...
        AssertionError: DeprecationWarning not issued

    If the warning has the right class, any additional tests that have been
    configured on the context, will be called:

        >>> from warnings import warn
        >>> def test(warning):
        ...     return False
        >>> context.add_test(test)
        >>> with context:
        ...     warn("Wrong Message", DeprecationWarning)
        Traceback (most recent call last):
            ...
        AssertionError: DeprecationWarning not issued

    """

    def __init__(self, warning_class, msg_fmt="{msg}"):
        self._warning_class = warning_class
        self._msg_fmt = msg_fmt
        self._warning_context = None
        self._warnings = []
        self._tests = []

    def __enter__(self):
        self._warning_context = catch_warnings(record=True)
        self._warnings = self._warning_context.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._warning_context.__exit__(exc_type, exc_val, exc_tb)
        if not any(self._is_expected_warning(w) for w in self._warnings):
            fail(self.format_message())

    def format_message(self):
        msg = "{} not issued".format(self._warning_class.__name__)
        return self._msg_fmt.format(
            msg=msg,
            exc_type=self._warning_class,
            exc_name=self._warning_class.__name__,
        )

    def _is_expected_warning(self, warning):
        if not issubclass(warning.category, self._warning_class):
            return False
        return all(test(warning) for test in self._tests)

    def add_test(self, cb):
        """Add a test callback.

        This callback is called after determining that the right warning
        class was issued. The callback will get the issued warning as only
        argument and must return a boolean value.

        """
        self._tests.append(cb)


class AssertWarnsRegexContext(AssertWarnsContext):

    """A context manager to test for warnings and their messages."""

    def __init__(self, warning_class, pattern, msg_fmt="{msg}"):
        super(AssertWarnsRegexContext, self).__init__(warning_class, msg_fmt)
        self.pattern = pattern

    def format_message(self):
        msg = "no {} matching {} issued".format(
            self._warning_class.__name__, repr(self.pattern)
        )
        return self._msg_fmt.format(
            msg=msg,
            exc_type=self._warning_class,
            exc_name=self._warning_class.__name__,
            pattern=self.pattern,
        )


def assert_warns(warning_type, msg_fmt="{msg}"):
    """Fail unless a specific warning is issued inside the context.

    If a different type of warning is issued, it will not be caught.

    >>> from warnings import warn
    >>> with assert_warns(UserWarning):
    ...     warn("warning message", UserWarning)
    ...
    >>> with assert_warns(UserWarning):
    ...     pass
    ...
    Traceback (most recent call last):
        ...
    AssertionError: UserWarning not issued
    >>> with assert_warns(UserWarning):
    ...     warn("warning message", UnicodeWarning)
    ...
    Traceback (most recent call last):
        ...
    AssertionError: UserWarning not issued

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * exc_type - exception type
    * exc_name - exception type name
    """
    return AssertWarnsContext(warning_type, msg_fmt)


def assert_warns_regex(warning_type, regex, msg_fmt="{msg}"):
    """Fail unless a warning with a message is issued inside the context.

    The message can be a regular expression string or object.

    >>> from warnings import warn
    >>> with assert_warns_regex(UserWarning, r"#\\d+"):
    ...     warn("Error #42", UserWarning)
    ...
    >>> with assert_warns_regex(UserWarning, r"Expected Error"):
    ...     warn("Generic Error", UserWarning)
    ...
    Traceback (most recent call last):
        ...
    AssertionError: no UserWarning matching 'Expected Error' issued

    The following msg_fmt arguments are supported:
    * msg - the default error message
    * exc_type - warning type
    * exc_name - warning type name
    * pattern - expected warning message as regular expression string
    """

    def test(warning):
        return re.search(regex, str(warning.message)) is not None

    context = AssertWarnsRegexContext(warning_type, regex, msg_fmt)
    context.add_test(test)
    return context


if sys.version_info >= (3,):
    _Str = str
else:
    _Str = unicode  # noqa: F821


def assert_json_subset(first, second):
    """Assert that a JSON object or array is a subset of another JSON object
    or array.

    The first JSON object or array must be supplied as a JSON-compatible
    dict or list, the JSON object or array to check must be a string, an
    UTF-8 bytes object, or a JSON-compatible list or dict.

    A JSON non-object, non-array value is the subset of another JSON value,
    if they are equal.

    A JSON object is the subset of another JSON object if for each name/value
    pair in the former there is a name/value pair in the latter with the same
    name. Additionally the value of the former pair must be a subset of the
    value of the latter pair.

    A JSON array is the subset of another JSON array, if they have the same
    number of elements and each element in the former is a subset of the
    corresponding element in the latter.

    >>> assert_json_subset({}, '{}')
    >>> assert_json_subset({}, '{"foo": "bar"}')
    >>> assert_json_subset({"foo": "bar"}, '{}')
    Traceback (most recent call last):
    ...
    AssertionError: element 'foo' missing from element $
    >>> assert_json_subset([1, 2], '[1, 2]')
    >>> assert_json_subset([2, 1], '[1, 2]')
    Traceback (most recent call last):
    ...
    AssertionError: element $[0] differs: 2 != 1
    >>> assert_json_subset([{}], '[{"foo": "bar"}]')
    >>> assert_json_subset({}, "INVALID JSON")
    Traceback (most recent call last):
    ...
    json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    """

    if not isinstance(second, (dict, list, str, bytes)):
        raise TypeError("second must be dict, list, str, or bytes")
    if isinstance(second, bytes):
        second = second.decode("utf-8")
    if isinstance(second, _Str):
        parsed_second = json_loads(second)
    else:
        parsed_second = second

    if not isinstance(parsed_second, (dict, list)):
        raise AssertionError(
            "second must decode to dict or list, not {}".format(
                type(parsed_second)
            )
        )

    comparer = _JSONComparer(_JSONPath("$"), first, parsed_second)
    comparer.assert_()


class _JSONComparer:
    def __init__(self, path, expected, actual):
        self._path = path
        self._expected = expected
        self._actual = actual

    def assert_(self):
        self._assert_types_are_equal()
        if isinstance(self._expected, dict):
            self._assert_dicts_equal()
        elif isinstance(self._expected, list):
            self._assert_arrays_equal()
        else:
            self._assert_fundamental_values_equal()

    def _assert_types_are_equal(self):
        if self._types_differ():
            self._raise_different_values()

    def _types_differ(self):
        if self._expected is None:
            return self._actual is not None
        elif isinstance(self._expected, (int, float)):
            return not isinstance(self._actual, (int, float))
        for type_ in [bool, str, _Str, list, dict]:
            if isinstance(self._expected, type_):
                return not isinstance(self._actual, type_)
        else:
            raise TypeError("unsupported type {}".format(type(self._expected)))

    def _assert_dicts_equal(self):
        self._assert_all_expected_keys_in_actual_dict()
        for name in self._expected:
            self._assert_json_value_equals_with_item(name)

    def _assert_all_expected_keys_in_actual_dict(self):
        keys = set(self._expected.keys()).difference(self._actual.keys())
        if keys:
            self._raise_missing_element(keys)

    def _assert_arrays_equal(self):
        if len(self._expected) != len(self._actual):
            self._raise_different_sizes()
        for i in range(len(self._expected)):
            self._assert_json_value_equals_with_item(i)

    def _assert_json_value_equals_with_item(self, item):
        path = self._path.append(item)
        expected = self._expected[item]
        actual = self._actual[item]
        _JSONComparer(path, expected, actual).assert_()

    def _assert_fundamental_values_equal(self):
        if self._expected != self._actual:
            self._raise_different_values()

    def _raise_different_values(self):
        self._raise_assertion_error(
            "element {path} differs: {expected} != {actual}"
        )

    def _raise_different_sizes(self):
        self._raise_assertion_error(
            "JSON array {path} differs in size: "
            "{expected_len} != {actual_len}",
            expected_len=len(self._expected),
            actual_len=len(self._actual),
        )

    def _raise_missing_element(self, keys):
        if len(keys) == 1:
            format_string = "element {elements} missing from element {path}"
            elements = repr(next(iter(keys)))
        else:
            format_string = "elements {elements} missing from element {path}"
            sorted_keys = sorted(keys)
            elements = (
                ", ".join(repr(k) for k in sorted_keys[:-1])
                + ", and "
                + repr(sorted_keys[-1])
            )
        self._raise_assertion_error(format_string, elements=elements)

    def _raise_assertion_error(self, format_, **kwargs):
        kwargs.update(
            {
                "path": self._path,
                "expected": repr(self._expected),
                "actual": repr(self._actual),
            }
        )
        raise AssertionError(format_.format(**kwargs))


class _JSONPath:
    def __init__(self, path):
        self._path = path

    def __str__(self):
        return self._path

    def append(self, item):
        return _JSONPath("{0}[{1}]".format(self._path, repr(item)))
