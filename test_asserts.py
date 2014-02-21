from datetime import datetime, timedelta
from unittest import TestCase

from asserts import (fail,
                     assert_is_none,
                     assert_is_not_none,
                     assert_true,
                     assert_false,
                     assert_boolean_true,
                     assert_boolean_false,
                     assert_is,
                     assert_is_not,
                     assert_is_instance,
                     assert_equal,
                     assert_not_equal,
                     assert_in,
                     assert_not_in,
                     assert_raises,
                     assert_raises_regex,
                     assert_raises_errno,
                     assert_succeeds,
                     assert_between,
                     assert_datetime_about_now,
                     assert_datetime_about_now_utc,
                     )


class _DummyObject(object):

    def __init__(self, value="x"):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


class AssertTest(TestCase):

    @staticmethod
    def _test_assertion_fails(cb):
        try:
            cb()
        except AssertionError as exc:
            return exc
        else:
            raise AssertionError("AssertionError not raised")

    def test_fail(self):
        assert_raises(AssertionError, fail)

    def test_fail__with_message(self):
        def cb():
            fail("foo")
        exc = self._test_assertion_fails(cb)
        assert_equal("foo", str(exc))

    def test_assert_true__default_message(self):
        with assert_raises_regex(AssertionError, r"^'' is not true$"):
            assert_true("")

    def test_assert_false__default_message(self):
        with assert_raises_regex(AssertionError, r"^25 is not false$"):
            assert_false(25)

    def test_assert_boolean_true__true(self):
        with assert_succeeds(AssertionError):
            assert_boolean_true(True)

    def test_assert_boolean_true__false(self):
        with assert_raises(AssertionError):
            assert_boolean_true(False)

    def test_assert_boolean_true__non_boolean_true(self):
        with assert_raises(AssertionError):
            assert_boolean_true(1)

    def test_assert_boolean_true__default_message(self):
        with assert_raises_regex(AssertionError, r"^True is not 1$"):
            assert_boolean_true(1)

    def test_assert_boolean_true__custom_message(self):
        with assert_raises_regex(AssertionError, r"^foo$"):
            assert_boolean_true(1, "foo")

    def test_assert_boolean_false__false(self):
        with assert_succeeds(AssertionError):
            assert_boolean_false(False)

    def test_assert_boolean_false__true(self):
        with assert_raises(AssertionError):
            assert_boolean_false(True)

    def test_assert_boolean_false__non_boolean_false(self):
        with assert_raises(AssertionError):
            assert_boolean_false(0)

    def test_assert_boolean_false__default_message(self):
        with assert_raises_regex(AssertionError, r"^False is not 0$"):
            assert_boolean_false(0)

    def test_assert_boolean_false__custom_message(self):
        with assert_raises_regex(AssertionError, r"^foo$"):
            assert_boolean_false(0, "foo")

    def test_assert_is_none__none(self):
        with assert_succeeds(AssertionError):
            assert_is_none(None)

    def test_assert_is_none__not_none(self):
        with assert_raises(AssertionError):
            assert_is_none("foo")

    def test_assert_is_not_none__not_none(self):
        with assert_succeeds(AssertionError):
            assert_is_not_none("foo")

    def test_assert_is_not_none__none(self):
        with assert_raises(AssertionError):
            assert_is_not_none(None)

    def test_assert_not_equal__success(self):
        with assert_succeeds(AssertionError):
            assert_not_equal("abc", "def")

    def test_assert_not_equal__fail(self):
        with assert_raises(AssertionError):
            assert_not_equal("abc", "abc")

    def test_assert_is__same(self):
        x = _DummyObject()
        assert_is(x, x)

    def test_assert_is__not_same(self):
        x = _DummyObject("x")
        y = _DummyObject("y")
        with assert_raises(AssertionError):
            assert_is(x, y)

    def test_assert_is__equal_but_not_same(self):
        x = _DummyObject("x")
        y = _DummyObject("x")
        with assert_raises(AssertionError):
            assert_is(x, y)

    def test_assert_is_not__not_same(self):
        x = _DummyObject()
        y = _DummyObject()
        with assert_succeeds(AssertionError):
            assert_is_not(x, y)

    def test_assert_is_not__same(self):
        x = _DummyObject("x")
        with assert_raises(AssertionError):
            assert_is_not(x, x)

    def test_assert_in__contains(self):
        with assert_succeeds(AssertionError):
            assert_in("foo", ["foo", "bar", "baz"])

    def test_assert_in__does_not_contain__default_message(self):
        with assert_raises_regex(AssertionError, r"^'foo' not in \[\]$"):
            assert_in("foo", [])

    def test_assert_in__does_not_contain__custom_message(self):
        with assert_raises_regex(AssertionError, r"^my message$"):
            assert_in("foo", [], "my message")

    def test_assert_not_in__does_not_contain(self):
        with assert_succeeds(AssertionError):
            assert_not_in("foo", [])

    def test_assert_not_in__does_contain__default_message(self):
        with assert_raises_regex(AssertionError,
                                 r"^'foo' is in \['foo', 'bar', 'baz'\]$"):
            assert_not_in("foo", ["foo", "bar", "baz"])

    def test_assert_not_in__does_contain__custom_message(self):
        with assert_raises_regex(AssertionError, r"^my message$"):
            assert_not_in("foo", ["foo", "bar", "baz"], "my message")

    def test_assert_between__equals_lower(self):
        with assert_succeeds(AssertionError):
            assert_between(0, 10, 0)

    def test_assert_between__equals_upper(self):
        with assert_succeeds(AssertionError):
            assert_between(0, 10, 10)

    def test_assert_between__between(self):
        with assert_succeeds(AssertionError):
            assert_between(0, 10, 5)

    def test_assert_between__too_low__default_message(self):
        with assert_raises_regex(AssertionError,
                                 r"^-1 is not between 0 and 10$"):
            assert_between(0, 10, -1)

    def test_assert_between__too_high__custom_message(self):
        with assert_raises_regex(AssertionError, r"^my message$"):
            assert_between(0, 10, 11, msg="my message")

    def test_assert_is_instance__is_instance(self):
        with assert_succeeds(AssertionError):
            assert_is_instance(4, int)

    def test_assert_is_instance__is_sub_class(self):
        with assert_succeeds(AssertionError):
            assert_is_instance(IOError(), Exception)

    def test_assert_is_instance__not_instance__default_message(self):
        with assert_raises_regex(AssertionError,
                                 "^'my string' is of <(type|class) 'str'> "
                                 "not of <(type|class) 'int'>$"):
            assert_is_instance("my string", int)

    def test_assert_is_instance__custom_message(self):
        with assert_raises_regex(AssertionError, r"^my message$"):
            assert_is_instance("my string", int, "my message")

    def test_assert_datetime_about_now__close(self):
        with assert_succeeds(AssertionError):
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

    def test_assert_datetime_about_now_utc__close(self):
        with assert_succeeds(AssertionError):
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

    def test_assert_raises__raises_right_exception(self):
        with assert_raises(KeyError):
            raise KeyError()

    def test_assert_raises__raises_subclass(self):
        class MyError(IndexError):
            pass
        with assert_raises(IndexError):
            raise MyError()

    def test_assert_raises__exception_not_thrown__default_message(self):
        try:
            with assert_raises(KeyError):
                pass
        except AssertionError as exc:
            assert_equal("KeyError not raised", str(exc))
        else:
            fail("AssertionError not thrown")

    def test_assert_raises__exception_not_thrown__custom_message(self):
        try:
            with assert_raises(KeyError, msg="Test Message"):
                pass
        except AssertionError as exc:
            assert_equal("Test Message", str(exc))
        else:
            fail("AssertionError not thrown")

    def test_assert_raises__wrong_exception_thrown(self):
        try:
            with assert_raises(IndexError):
                raise KeyError()
        except KeyError:
            pass
        except Exception as exc:
            fail(str(exc) + " was raised")

    def test_assert_raises_errno__right_errno(self):
        with assert_succeeds(AssertionError):
            with assert_raises_errno(OSError, 20):
                raise OSError(20, "Test message")

    def test_assert_raises_errno__no_exception_thrown(self):
        with assert_raises(AssertionError):
            with assert_raises_errno(OSError, 20):
                pass

    def test_assert_raises_errno__wrong_class(self):
        class RightClass(OSError):
            pass

        class WrongClass(OSError):
            pass

        with assert_raises(WrongClass):
            with assert_raises_errno(RightClass, 20):
                raise WrongClass(20, "Test message")

    def test_assert_raises_errno__wrong_errno(self):
        with assert_raises(AssertionError):
            with assert_raises_errno(OSError, 20):
                raise OSError(1, "Test message")

    def test_assert_succeeds__no_exception_thrown(self):
        with assert_succeeds(KeyError):
            pass

    def test_assert_succeeds__expected_exception__default_message(self):
        with assert_raises_regex(AssertionError,
                                 r"^KeyError was unexpectedly raised$"):
            with assert_succeeds(KeyError):
                raise KeyError()

    def test_assert_succeeds__unexpected_exception(self):
        with assert_raises(KeyError):
            with assert_succeeds(ValueError):
                raise KeyError()
