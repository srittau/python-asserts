from datetime import datetime, timedelta
import re
from unittest import TestCase
import sys

from asserts import (fail,
                     assert_true,
                     assert_false,
                     assert_boolean_true,
                     assert_boolean_false,
                     assert_is_none,
                     assert_is_not_none,
                     assert_equal,
                     assert_not_equal,
                     assert_almost_equal,
                     assert_between,
                     assert_is,
                     assert_is_not,
                     assert_in,
                     assert_not_in,
                     assert_regex,
                     assert_is_instance,
                     assert_has_attr,
                     assert_datetime_about_now,
                     assert_datetime_about_now_utc,
                     assert_raises,
                     assert_raises_regex,
                     assert_raises_errno,
                     assert_succeeds,
                     )


class _DummyObject(object):

    def __init__(self, value="x"):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return "<Dummy>"


def _assert_raises_assertion(expected_message):
    """Fail if the context does not raise an AssertionError or the exception
    message does not match.

    This is used to test assertions, without using those assertions.

    """

    class Context(object):

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                raise AssertionError("no AssertionError raised")
            if exc_type != AssertionError:
                return False
            if str(exc_val) != expected_message:
                raise AssertionError(
                    "expected exception message {!r}, got {!r}".format(
                        expected_message, str(exc_val)
                    ))
            return True

    return Context()


class AssertTest(TestCase):

    def test_fail__default_message(self):
        with _assert_raises_assertion("assertion failure"):
            fail()

    def test_fail__with_message(self):
        with _assert_raises_assertion("test message"):
            fail("test message")

    def test_assert_true__truthy_value(self):
        assert_true("Hello World!")

    def test_assert_true__falsy_value__default_message(self):
        with _assert_raises_assertion("'' is not truthy"):
            assert_true("")

    def test_assert_true__falsy_value__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_true("", msg="test message")

    def test_assert_false__falsy_value(self):
        assert_false("")

    def test_assert_false__truthy_value__default_message(self):
        with _assert_raises_assertion("25 is not falsy"):
            assert_false(25)

    def test_assert_false__truthy_value__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_false(25, msg="test message")

    def test_assert_boolean_true__true(self):
        assert_boolean_true(True)

    def test_assert_boolean_true__false__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_boolean_true(False, msg="test message")

    def test_assert_boolean_true__truthy__default_message(self):
        with _assert_raises_assertion("1 is not True"):
            assert_boolean_true(1)

    def test_assert_boolean_false__false(self):
        assert_boolean_false(False)

    def test_assert_boolean_false__true__default_message(self):
        with _assert_raises_assertion("'foo' is not False"):
            assert_boolean_false("foo")

    def test_assert_boolean_false__falsy__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_boolean_false(0, msg="test message")

    def test_assert_is_none__none(self):
        assert_is_none(None)

    def test_assert_is_none__string__default_message(self):
        with _assert_raises_assertion("'' is not None"):
            assert_is_none("")

    def test_assert_is_none__int__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_is_none(55, msg="test message")

    def test_assert_is_not_none__string(self):
            assert_is_not_none("")

    def test_assert_is_not_none__none__default_message(self):
        with _assert_raises_assertion("expected value not to be None"):
            assert_is_not_none(None)

    def test_assert_is_not_none__none__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_is_not_none(None, msg="test message")

    def test_assert_equal__equal_strings(self):
        assert_equal("foo", "foo")

    def test_assert_equal__equal_objects(self):
        class MyClass(object):
            def __eq__(self, other):
                return True
        assert_equal(MyClass(), MyClass())

    def test_assert_equal__not_equal__default_message(self):
        with _assert_raises_assertion("'string' != 55"):
            assert_equal("string", 55)

    def test_assert_equal__not_equal__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_equal("string", 55, msg="test message")

    def test_assert_not_equal__not_equal(self):
        assert_not_equal("abc", "def")

    def test_assert_not_equal__equal__default_message(self):
        with _assert_raises_assertion("'abc' == 'abc'"):
            assert_not_equal("abc", "abc")

    def test_assert_not_equal__equal__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_not_equal("abc", "abc", msg="test message")

    def test_assert_almost_equal__same(self):
        assert_almost_equal(5, 5)

    def test_assert_almost_equal__similar__defaults(self):
        assert_almost_equal(5, 5.00000001)

    def test_assert_almost_equal__similar__places(self):
        assert_almost_equal(5, 5.0001, places=3)

    def test_assert_almost_equal__similar__delta(self):
        assert_almost_equal(5, 5.001, delta=0.1)

    def test_assert_almost_equal__not_similar__default_message(self):
        with _assert_raises_assertion("5 != 5.0001 within 7 places"):
            assert_almost_equal(5, 5.0001)

    def test_assert_almost_equal__not_similar__places__default_message(self):
        with _assert_raises_assertion("5 != 6 within 3 places"):
            assert_almost_equal(5, 6, places=3)

    def test_assert_almost_equal__not_similar__delta__default_message(self):
        with _assert_raises_assertion("5 != 6 with delta=0.1"):
            assert_almost_equal(5, 6, delta=0.1)

    def test_assert_almost_equal__not_similar__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_almost_equal(5, -5, msg="test message")

    def test_assert_almost_equal__wrong_types(self):
        try:
            assert_almost_equal("5", "5")
        except TypeError:
            pass
        else:
            raise AssertionError("TypeError not raised")

    def test_assert_almost_equal__places_and_delta(self):
        try:
            assert_almost_equal(5, 5, places=3, delta=0.0003)
        except TypeError:
            pass
        else:
            raise AssertionError("TypeError not raised")

    def test_assert_regex__matches_string(self):
        assert_regex("This is a test text", "is.*test")

    def test_assert_regex__matches_regex(self):
        regex = re.compile("is.*test")
        assert_regex("This is a test text", regex)

    def test_assert_regex__does_not_match_string__default_message(self):
        with _assert_raises_assertion(
                "'This is a test text' does not match 'XXX'"):
            assert_regex("This is a test text", "XXX")

    def test_assert_regex__does_not_match_regex__default_message(self):
        regex = re.compile(r"XXX")
        with _assert_raises_assertion(
                "'This is a test text' does not match 'XXX'"):
            assert_regex("This is a test text", regex)

    def test_assert_regex__does_not_match__custom_message(self):
        with _assert_raises_assertion("test message"):
            assert_regex("This is a test text", "XXX", msg="test message")

    def test_assert_is__same(self):
        x = _DummyObject()
        assert_is(x, x)

    def test_assert_is__not_same__default_message(self):
        with _assert_raises_assertion("'x' is not 'y'"):
            assert_is("x", "y")

    def test_assert_is__equal_but_not_same__custom_message(self):
        x = _DummyObject("x")
        y = _DummyObject("x")
        with _assert_raises_assertion("test message"):
            assert_is(x, y, msg="test message")

    def test_assert_is_not__not_same(self):
        x = _DummyObject()
        y = _DummyObject()
        assert_is_not(x, y)

    def test_assert_is_not__same__default_message(self):
        with _assert_raises_assertion("expected value not to be 5"):
            assert_is_not(5, 5)

    def test_assert_is_not__same__custom_message(self):
        x = _DummyObject("x")
        with _assert_raises_assertion("test message"):
            assert_is_not(x, x, msg="test message")

    def test_assert_in__contains(self):
        assert_in("foo", ["foo", "bar", "baz"])

    def test_assert_in__does_not_contain__default_message(self):
        with _assert_raises_assertion("'foo' not in []"):
            assert_in("foo", [])

    def test_assert_in__does_not_contain__custom_message(self):
        with _assert_raises_assertion("my message"):
            assert_in("foo", [], "my message")

    def test_assert_not_in__does_not_contain(self):
        assert_not_in("foo", [])

    def test_assert_not_in__does_contain__default_message(self):
        with _assert_raises_assertion("'foo' is in ['foo', 'bar', 'baz']"):
            assert_not_in("foo", ["foo", "bar", "baz"])

    def test_assert_not_in__does_contain__custom_message(self):
        with _assert_raises_assertion("my message"):
            assert_not_in("foo", ["foo", "bar", "baz"], "my message")

    def test_assert_between__within_range(self):
        assert_between(0, 10, 0)
        assert_between(0, 10, 10)
        assert_between(0, 10, 5)

    def test_assert_between__too_low__default_message(self):
        with _assert_raises_assertion("-1 is not between 0 and 10"):
            assert_between(0, 10, -1)

    def test_assert_between__too_high__custom_message(self):
        with _assert_raises_assertion("my message"):
            assert_between(0, 10, 11, msg="my message")

    def test_assert_is_instance__is_instance(self):
        assert_is_instance(4, int)

    def test_assert_is_instance__is_sub_class(self):
        assert_is_instance(IOError(), Exception)

    def test_assert_is_instance__not_instance__default_message(self):
        expected_message = ("'my string' is of <class 'str'>, "
                            "expected <class 'int'>")
        if sys.version_info[0] < 3:
            expected_message = expected_message.replace("class", "type")
        with _assert_raises_assertion(expected_message):
            assert_is_instance("my string", int)

    def test_assert_is_instance__custom_message(self):
        with _assert_raises_assertion("my message"):
            assert_is_instance("my string", int, msg="my message")

    def test_assert_has_attr__has_attribute(self):
        d = _DummyObject()
        d.foo = 5
        assert_has_attr(d, "foo")

    def test_assert_has_attr__does_not_have_attribute__default_message(self):
        d = _DummyObject()
        with _assert_raises_assertion("<Dummy> is missing attribute 'foo'"):
            assert_has_attr(d, "foo")

    def test_assert_has_attr__does_not_have_attribute__custom_message(self):
        d = _DummyObject()
        with _assert_raises_assertion("test message"):
            assert_has_attr(d, "foo", msg="test message")

    def test_assert_datetime_about_now__close(self):
        assert_datetime_about_now(datetime.now())

    def test_assert_datetime_about_now__too_low(self):
        then = datetime.now() - timedelta(minutes=1)
        with assert_raises(AssertionError):
            assert_datetime_about_now(then)

    def test_assert_datetime_about_now__too_high(self):
        then = datetime.now() + timedelta(minutes=1)
        with assert_raises(AssertionError):
            assert_datetime_about_now(then)

    def test_assert_datetime_about_now__default_message(self):
        then = datetime(1990, 4, 13, 12, 30, 15)
        expected_message = (r"^datetime.datetime\(1990, 4, 13, 12, 30, 15\) "
                            "is not close to current "
                            "datetime.datetime"
                            "\(\d+, \d+, \d+, \d+, \d+, \d+, \d+\)$")
        with assert_raises_regex(AssertionError, expected_message):
            assert_datetime_about_now(then)

    def test_assert_datetime_about_now__custom_message(self):
        then = datetime(1990, 4, 13, 12, 30, 15)
        with _assert_raises_assertion("test message"):
            assert_datetime_about_now(then, msg="test message")

    def test_assert_datetime_about_now_utc__close(self):
        assert_datetime_about_now_utc(datetime.utcnow())

    def test_assert_datetime_about_now_utc__too_low(self):
        then = datetime.utcnow() - timedelta(minutes=1)
        with assert_raises(AssertionError):
            assert_datetime_about_now_utc(then)

    def test_assert_datetime_about_now_utc__too_high(self):
        then = datetime.utcnow() + timedelta(minutes=1)
        with assert_raises(AssertionError):
            assert_datetime_about_now_utc(then)

    def assert_datetime_about_now_utc__default_message(self):
        then = datetime(1990, 4, 13, 12, 30, 15)
        expected_message = (
            r"datetime.datetime\(1990, 4, 13, 12, 30, 15\) "
            r"is not close to current UTC "
            r"datetime.datetime\(\d+, \d+, \d+, \d+, \d+, \d+\)$")
        with assert_raises_regex(AssertionError, expected_message):
            assert_datetime_about_now_utc(then)

    def test_assert_datetime_about_now_utc__custom_message(self):
        then = datetime(1990, 4, 13, 12, 30, 15)
        with _assert_raises_assertion("test message"):
            assert_datetime_about_now_utc(then, msg="test message")

    def test_assert_raises__raises_right_exception(self):
        with assert_raises(KeyError):
            raise KeyError()

    def test_assert_raises__raises_subclass(self):
        class MyError(IndexError):
            pass
        with assert_raises(IndexError):
            raise MyError()

    def test_assert_raises__exception_not_raised__default_message(self):
        with _assert_raises_assertion("KeyError not raised"):
            with assert_raises(KeyError):
                pass

    def test_assert_raises__exception_not_raised__custom_message(self):
        with _assert_raises_assertion("test message"):
            with assert_raises(KeyError, msg="test message"):
                pass

    def test_assert_raises__wrong_exception_raised(self):
        try:
            with assert_raises(IndexError):
                raise KeyError()
        except KeyError:
            pass
        except Exception as exc:
            fail(str(exc) + " was raised")

    def test_assert_raises_errno__right_errno(self):
        with assert_raises_errno(OSError, 20):
            raise OSError(20, "Test error")

    def test_assert_raises_errno__no_exception_raised__default_message(self):
        with _assert_raises_assertion("OSError not raised"):
            with assert_raises_errno(OSError, 20):
                pass

    def test_assert_raises_errno__no_exception_raised__custom_message(self):
        with _assert_raises_assertion("test message"):
            with assert_raises_errno(OSError, 20, msg="test message"):
                pass

    def test_assert_raises_errno__wrong_class_raised(self):
        class RightClass(OSError):
            pass

        class WrongClass(OSError):
            pass

        try:
            with assert_raises_errno(RightClass, 20):
                raise WrongClass(20, "Test error")
        except WrongClass:
            pass
        else:
            raise AssertionError("WrongClass was not raised")

    def test_assert_raises_errno__wrong_errno__default_message(self):
        with _assert_raises_assertion("wrong errno: 20 != 1"):
            with assert_raises_errno(OSError, 20):
                raise OSError(1, "Test error")

    def test_assert_raises_errno__wrong_errno__custom_message(self):
        with _assert_raises_assertion("test message"):
            with assert_raises_errno(OSError, 20, msg="test message"):
                raise OSError(1, "Test error")

    def test_assert_succeeds__no_exception_raised(self):
        with assert_succeeds(KeyError):
            pass

    def test_assert_succeeds__expected_exception__default_message(self):
        with _assert_raises_assertion("KeyError was unexpectedly raised"):
            with assert_succeeds(KeyError):
                raise KeyError()

    def test_assert_succeeds__expected_exception__custom_message(self):
        with _assert_raises_assertion("test message"):
            with assert_succeeds(KeyError, msg="test message"):
                raise KeyError()

    def test_assert_succeeds__unexpected_exception(self):
        try:
            with assert_succeeds(ValueError):
                raise KeyError()
        except KeyError:
            pass
        else:
            raise AssertionError("KeyError was not raised")
