# -*- coding: utf-8 -*-

import re
import sys
from collections import OrderedDict
from datetime import datetime, timedelta
from unittest import TestCase
from warnings import warn, catch_warnings

from asserts import (
    fail,
    assert_true,
    assert_false,
    assert_boolean_true,
    assert_boolean_false,
    assert_is_none,
    assert_is_not_none,
    assert_equal,
    assert_not_equal,
    assert_almost_equal,
    assert_not_almost_equal,
    assert_dict_equal,
    assert_dict_superset,
    assert_less,
    assert_less_equal,
    assert_greater,
    assert_greater_equal,
    assert_between,
    assert_is,
    assert_is_not,
    assert_in,
    assert_not_in,
    assert_count_equal,
    assert_regex,
    assert_is_instance,
    assert_not_is_instance,
    assert_has_attr,
    assert_datetime_about_now,
    assert_datetime_about_now_utc,
    assert_raises,
    assert_raises_regex,
    assert_raises_errno,
    assert_succeeds,
    assert_warns,
    assert_warns_regex,
    assert_json_subset,
)


class Box:
    def __init__(self, initial_value):
        self.value = initial_value


class _DummyObject(object):
    def __init__(self, value="x"):
        self.value = value

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
                    )
                )
            return True

    return Context()


class AssertTest(TestCase):
    _type_string = "type" if sys.version_info[0] < 3 else "class"

    # fail()

    def test_fail__default_message(self):
        with _assert_raises_assertion("assertion failure"):
            fail()

    def test_fail__with_message(self):
        with _assert_raises_assertion("test message"):
            fail("test message")

    # assert_true()

    def test_assert_true__truthy_value(self):
        assert_true("Hello World!")

    def test_assert_true__falsy_value__default_message(self):
        with _assert_raises_assertion("'' is not truthy"):
            assert_true("")

    def test_assert_true__falsy_value__custom_message(self):
        with _assert_raises_assertion("0 is not truthy;0"):
            assert_true(0, "{msg};{expr}")

    # assert_false()

    def test_assert_false__falsy_value(self):
        assert_false("")

    def test_assert_false__truthy_value__default_message(self):
        with _assert_raises_assertion("25 is not falsy"):
            assert_false(25)

    def test_assert_false__truthy_value__custom_message(self):
        with _assert_raises_assertion("'foo' is not falsy;foo"):
            assert_false("foo", "{msg};{expr}")

    # assert_boolean_true()

    def test_assert_boolean_true__true(self):
        assert_boolean_true(True)

    def test_assert_boolean_true__false__custom_message(self):
        with _assert_raises_assertion("'Foo' is not True;Foo"):
            assert_boolean_true("Foo", "{msg};{expr}")

    def test_assert_boolean_true__truthy__default_message(self):
        with _assert_raises_assertion("1 is not True"):
            assert_boolean_true(1)

    # assert_boolean_false()

    def test_assert_boolean_false__false(self):
        assert_boolean_false(False)

    def test_assert_boolean_false__true__default_message(self):
        with _assert_raises_assertion("'foo' is not False"):
            assert_boolean_false("foo")

    def test_assert_boolean_false__falsy__custom_message(self):
        with _assert_raises_assertion("0 is not False;0"):
            assert_boolean_false(0, "{msg};{expr}")

    # assert_is_none()

    def test_assert_is_none__none(self):
        assert_is_none(None)

    def test_assert_is_none__string__default_message(self):
        with _assert_raises_assertion("'' is not None"):
            assert_is_none("")

    def test_assert_is_none__int__custom_message(self):
        with _assert_raises_assertion("55 is not None;55"):
            assert_is_none(55, "{msg};{expr}")

    # assert_is_not_none()

    def test_assert_is_not_none__string(self):
        assert_is_not_none("")

    def test_assert_is_not_none__none__default_message(self):
        with _assert_raises_assertion("expression is None"):
            assert_is_not_none(None)

    def test_assert_is_not_none__none__custom_message(self):
        with _assert_raises_assertion("expression is None;None"):
            assert_is_not_none(None, "{msg};{expr!r}")

    # assert_equal()

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
        with _assert_raises_assertion("'string' != 55;'string';55"):
            assert_equal("string", 55, "{msg};{first!r};{second!r}")

    def test_assert_equal__dict(self):
        with _assert_raises_assertion("key 'foo' missing from right dict"):
            assert_equal({"foo": 5}, {})

    # assert_not_equal()

    def test_assert_not_equal__not_equal(self):
        assert_not_equal("abc", "def")

    def test_assert_not_equal__equal__default_message(self):
        with _assert_raises_assertion("'abc' == 'abc'"):
            assert_not_equal("abc", "abc")

    def test_assert_not_equal__equal__custom_message(self):
        with _assert_raises_assertion("1.0 == 1;1.0;1"):
            assert_not_equal(1.0, 1, "{msg};{first};{second}")

    # assert_almost_equal()

    def test_assert_almost_equal__same(self):
        assert_almost_equal(5, 5)

    def test_assert_almost_equal__similar__defaults(self):
        assert_almost_equal(5, 5.00000001)

    def test_assert_almost_equal__similar__places(self):
        assert_almost_equal(5, 5.0001, places=3)

    def test_assert_almost_equal__similar__delta(self):
        assert_almost_equal(5, 5.001, delta=0.1)

    def test_assert_almost_equal__similar__delta_reverse(self):
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

    def test_assert_almost_equal__not_similar__delta_reverse(self):
        with _assert_raises_assertion("6 != 5 with delta=0.3"):
            assert_almost_equal(6, 5, delta=0.3)

    def test_assert_almost_equal__not_similar__custom_message(self):
        with _assert_raises_assertion("5 != -5 within 7 places;5;-5;7;None"):
            assert_almost_equal(
                5, -5, msg_fmt="{msg};{first};{second};{places};{delta!r}"
            )

    def test_assert_almost_equal__not_similar__places__custom_message(self):
        with _assert_raises_assertion("5 != -5 within 3 places;5;-5;3;None"):
            assert_almost_equal(
                5,
                -5,
                places=3,
                msg_fmt="{msg};{first};{second};{places};{delta!r}",
            )

    def test_assert_almost_equal__not_similar__delta__custom_message(self):
        with _assert_raises_assertion("5 != 6 with delta=0.1;5;6;None;0.1"):
            assert_almost_equal(
                5,
                6,
                delta=0.1,
                msg_fmt="{msg};{first};{second};{places!r};{delta}",
            )

    def test_assert_almost_equal__wrong_types(self):
        try:
            assert_almost_equal("5", "5")  # type: ignore
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

    def test_assert_almost_equal__delta_eq_0(self):
        try:
            assert_almost_equal(5, 5, delta=0)
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError not raised")

    def test_assert_almost_equal__delta_lt_0(self):
        try:
            assert_almost_equal(5, 5, delta=-1)
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError not raised")

    # assert_not_almost_equal()

    def test_assert_not_almost_equal__same(self):
        with _assert_raises_assertion("5 == 5 within 7 places"):
            assert_not_almost_equal(5, 5)

    def test_assert_not_almost_equal__similar__defaults(self):
        with _assert_raises_assertion("5 == 5.00000001 within 7 places"):
            assert_not_almost_equal(5, 5.00000001)

    def test_assert_not_almost_equal__similar__places(self):
        with _assert_raises_assertion("5 == 5.0001 within 3 places"):
            assert_not_almost_equal(5, 5.0001, places=3)

    def test_assert_not_almost_equal__similar__delta(self):
        with _assert_raises_assertion("5 == 5.1 with delta=0.1"):
            assert_not_almost_equal(5, 5.1, delta=0.1)

    def test_assert_not_almost_equal__similar__delta_reverse(self):
        with _assert_raises_assertion("5 != 6 with delta=0.3"):
            assert_almost_equal(5, 6, delta=0.3)

    def test_assert_not_almost_equal__not_similar(self):
        assert_not_almost_equal(5, 5.0001)

    def test_assert_not_almost_equal__not_similar__delta(self):
        assert_not_almost_equal(5, 5.1, delta=0.05)

    def test_assert_not_almost_equal__not_similar__delta_reverse(self):
        assert_not_almost_equal(5.1, 5, delta=0.05)

    def test_assert_not_almost_equal__similar__custom_message(self):
        with _assert_raises_assertion(
            "5 == 5.00000001 within 7 places;5;5.00000001;7;None"
        ):
            assert_not_almost_equal(
                5,
                5.00000001,
                msg_fmt="{msg};{first};{second};{places};{delta!r}",
            )

    def test_assert_not_almost_equal__similar__places__custom_message(self):
        with _assert_raises_assertion(
            "5 == 5.0001 within 3 places;5;5.0001;3;None"
        ):
            assert_not_almost_equal(
                5,
                5.0001,
                places=3,
                msg_fmt="{msg};{first};{second};{places};{delta!r}",
            )

    def test_assert_not_almost_equal__similar__delta__custom_message(self):
        with _assert_raises_assertion("5 == 6 with delta=1.1;5;6;None;1.1"):
            assert_not_almost_equal(
                5,
                6,
                delta=1.1,
                msg_fmt="{msg};{first};{second};{places!r};{delta}",
            )

    def test_assert_not_almost_equal__wrong_types(self):
        try:
            assert_not_almost_equal("5", "5")  # type: ignore
        except TypeError:
            pass
        else:
            raise AssertionError("TypeError not raised")

    def test_assert_not_almost_equal__places_and_delta(self):
        try:
            assert_not_almost_equal(5, 5, places=3, delta=0.0003)
        except TypeError:
            pass
        else:
            raise AssertionError("TypeError not raised")

    def test_not_assert_almost_equal__delta_eq_0(self):
        try:
            assert_not_almost_equal(5, 5, delta=0)
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError not raised")

    def test_not_assert_almost_equal__delta_lt_0(self):
        try:
            assert_not_almost_equal(5, 5, delta=-1)
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError not raised")

    # assert_dict_equal()

    def test_assert_dict_equal__empty_dicts(self):
        assert_dict_equal({}, {})

    def test_assert_dict_equal__dicts_are_equal(self):
        assert_dict_equal({"foo": 5}, {"foo": 5})

    def test_assert_dict_equal__one_key_missing_from_right(self):
        with _assert_raises_assertion("key 'foo' missing from right dict"):
            assert_dict_equal({"bar": 10, "foo": 5}, {"bar": 10})

    def test_assert_dict_equal__multiple_keys_missing_from_right(self):
        with _assert_raises_assertion(
            "keys 'bar', 'foo' missing from right dict"
        ):
            assert_dict_equal({"foo": 5, "bar": 10, "baz": 15}, {"baz": 15})

    def test_assert_dict_equal__one_key_missing_from_left(self):
        with _assert_raises_assertion("extra key 'foo' in right dict"):
            assert_dict_equal({"bar": 10}, {"bar": 10, "foo": 5})

    def test_assert_dict_equal__multiple_keys_missing_from_left(self):
        with _assert_raises_assertion("extra keys 'bar', 'foo' in right dict"):
            assert_dict_equal({"baz": 15}, {"foo": 5, "bar": 10, "baz": 15})

    def test_assert_dict_equal__values_do_not_match(self):
        with _assert_raises_assertion("key 'foo' differs: 15 != 10"):
            assert_dict_equal({"foo": 15}, {"foo": 10})

    def test_assert_dict_equal__not_string_keys(self):
        with _assert_raises_assertion("key 10 missing from right dict"):
            assert_dict_equal({10: "foo"}, {})
        with _assert_raises_assertion("keys 'foo', 5 missing from right dict"):
            assert_dict_equal({5: "", "foo": ""}, {})
        with _assert_raises_assertion("extra key 10 in right dict"):
            assert_dict_equal({}, {10: "foo"})
        with _assert_raises_assertion("extra keys 'foo', 5 in right dict"):
            assert_dict_equal({}, {5: "", "foo": ""})

    def test_assert_dict_equal__message_precedence(self):
        with _assert_raises_assertion("key 'foo' missing from right dict"):
            assert_dict_equal(
                {"foo": "", "bar": "", "baz": 5},
                {"bar": "", "baz": 10, "extra": ""},
            )
        with _assert_raises_assertion("extra key 'extra' in right dict"):
            assert_dict_equal(
                {"bar": "", "baz": 5}, {"bar": "", "baz": 10, "extra": ""}
            )

    def test_assert_dict_equal__custom_key_message(self):
        with _assert_raises_assertion(
            "key 'foo' missing from right dict;"
            "{'foo': ''};{'bar': ''};['foo'];['bar']"
        ):
            assert_dict_equal(
                {"foo": ""},
                {"bar": ""},
                key_msg_fmt="{msg};{first!r};{second!r};"
                "{missing_keys!r};{extra_keys!r}",
            )

    def test_assert_dict_equal__custom_value_message(self):
        with _assert_raises_assertion(
            "key 'foo' differs: 5 != 10;{'foo': 5};{'foo': 10};" "'foo';5;10"
        ):
            assert_dict_equal(
                {"foo": 5},
                {"foo": 10},
                value_msg_fmt="{msg};{first!r};{second!r};"
                "{key!r};{first_value};{second_value}",
            )

    # assert_dict_superset()

    def test_assert_dict_superset__empty_dicts(self):
        assert_dict_superset({}, {})

    def test_assert_dict_superset__dicts_are_equal(self):
        assert_dict_superset({"foo": 5}, {"foo": 5})

    def test_assert_dict_superset__dicts_is_superset(self):
        assert_dict_superset({"foo": 5}, {"foo": 5, "bar": 10})

    def test_assert_dict_superset__one_key_missing_from_right(self):
        with _assert_raises_assertion("key 'foo' missing from right dict"):
            assert_dict_superset({"bar": 10, "foo": 5}, {"bar": 10})

    def test_assert_dict_superset__multiple_keys_missing_from_right(self):
        with _assert_raises_assertion(
            "keys 'bar', 'foo' missing from right dict"
        ):
            assert_dict_superset({"foo": 5, "bar": 10, "baz": 15}, {"baz": 15})

    def test_assert_dict_superset__values_do_not_match(self):
        with _assert_raises_assertion("key 'foo' differs: 15 != 10"):
            assert_dict_superset({"foo": 15}, {"foo": 10, "bar": 15})

    def test_assert_dict_superset__not_string_keys(self):
        with _assert_raises_assertion("key 10 missing from right dict"):
            assert_dict_superset({10: "foo"}, {})
        with _assert_raises_assertion("keys 'foo', 5 missing from right dict"):
            assert_dict_superset({5: "", "foo": ""}, {})

    def test_assert_dict_superset__message_precedence(self):
        with _assert_raises_assertion("key 'foo' missing from right dict"):
            assert_dict_superset({"foo": "", "bar": 5}, {"bar": 1})

    def test_assert_dict_superset__custom_key_message(self):
        with _assert_raises_assertion(
            "key 'foo' missing from right dict;"
            "{'foo': ''};{'bar': ''};['foo']"
        ):
            assert_dict_superset(
                {"foo": ""},
                {"bar": ""},
                key_msg_fmt="{msg};{first!r};{second!r};" "{missing_keys!r}",
            )

    def test_assert_dict_superset__custom_value_message(self):
        with _assert_raises_assertion(
            "key 'foo' differs: 5 != 10;{'foo': 5};{'foo': 10};" "'foo';5;10"
        ):
            assert_dict_superset(
                {"foo": 5},
                {"foo": 10},
                value_msg_fmt="{msg};{first!r};{second!r};"
                "{key!r};{first_value};{second_value}",
            )

    # assert_less()

    def test_assert_less(self):
        assert_less(4, 5)
        with _assert_raises_assertion("5 is not less than 5"):
            assert_less(5, 5)
        with _assert_raises_assertion("'foo' is not less than 'bar'"):
            assert_less("foo", "bar")
        with _assert_raises_assertion("6 is not less than 5;6;5"):
            assert_less(6, 5, "{msg};{first};{second}")

    # assert_less_equal()

    def test_assert_less_equal(self):
        assert_less_equal(4, 5)
        assert_less_equal(5, 5)
        with _assert_raises_assertion(
            "'foo' is not less than or equal to 'bar'"
        ):
            assert_less_equal("foo", "bar")
        with _assert_raises_assertion("6 is not less than or equal to 5;6;5"):
            assert_less_equal(6, 5, "{msg};{first};{second}")

    # assert_greater()

    def test_assert_greater(self):
        assert_greater(5, 4)
        with _assert_raises_assertion("5 is not greater than 5"):
            assert_greater(5, 5)
        with _assert_raises_assertion("'bar' is not greater than 'foo'"):
            assert_greater("bar", "foo")
        with _assert_raises_assertion("5 is not greater than 6;5;6"):
            assert_greater(5, 6, "{msg};{first};{second}")

    # assert_greater_equal()

    def test_assert_greater_equal(self):
        assert_greater_equal(5, 4)
        assert_greater_equal(5, 5)
        with _assert_raises_assertion(
            "'bar' is not greater than or equal to 'foo'"
        ):
            assert_greater_equal("bar", "foo")
        with _assert_raises_assertion(
            "5 is not greater than or equal to 6;5;6"
        ):
            assert_greater_equal(5, 6, "{msg};{first};{second}")

    # assert_regex()

    def test_assert_regex__matches_string(self):
        assert_regex("This is a test text", "is.*test")

    def test_assert_regex__matches_regex(self):
        regex = re.compile("is.*test")
        assert_regex("This is a test text", regex)

    def test_assert_regex__does_not_match_string__default_message(self):
        with _assert_raises_assertion(
            "'This is a test text' does not match 'not found'"
        ):
            assert_regex("This is a test text", "not found")

    def test_assert_regex__does_not_match_regex__default_message(self):
        regex = re.compile(r"not found")
        with _assert_raises_assertion(
            "'This is a test text' does not match 'not found'"
        ):
            assert_regex("This is a test text", regex)

    def test_assert_regex__does_not_match_string__custom_message(self):
        with _assert_raises_assertion(
            "'Wrong text' does not match 'not found';"
            "'Wrong text';'not found'"
        ):
            assert_regex(
                "Wrong text", r"not found", "{msg};{text!r};{pattern!r}"
            )

    def test_assert_regex__does_not_match_regex__custom_message(self):
        regex = re.compile(r"not found")
        with _assert_raises_assertion(
            "'Wrong text' does not match 'not found';'Wrong text';"
            "'not found'"
        ):
            assert_regex("Wrong text", regex, "{msg};{text!r};{pattern!r}")

    # assert_is()

    def test_assert_is__same(self):
        x = _DummyObject()
        assert_is(x, x)

    def test_assert_is__not_same__default_message(self):
        with _assert_raises_assertion("'x' is not 'y'"):
            assert_is("x", "y")

    def test_assert_is__equal_but_not_same__custom_message(self):
        x = "x"
        y = _DummyObject("y")
        with _assert_raises_assertion("'x' is not <Dummy>;'x';y"):
            assert_is(x, y, "{msg};{first!r};{second.value}")

    # assert_is_not()

    def test_assert_is_not__not_same(self):
        x = _DummyObject()
        y = _DummyObject()
        assert_is_not(x, y)

    def test_assert_is_not__same__default_message(self):
        x = _DummyObject("x")
        with _assert_raises_assertion("both arguments refer to <Dummy>"):
            assert_is_not(x, x)

    def test_assert_is_not__same__custom_message(self):
        x = _DummyObject("x")
        with _assert_raises_assertion("both arguments refer to <Dummy>;x;x"):
            assert_is_not(x, x, "{msg};{first.value};{second.value}")

    # assert_in()

    def test_assert_in__contains(self):
        assert_in("foo", ["foo", "bar", "baz"])

    def test_assert_in__does_not_contain__default_message(self):
        with _assert_raises_assertion("'foo' not in []"):
            assert_in("foo", [])

    def test_assert_in__does_not_contain__custom_message(self):
        with _assert_raises_assertion("'foo' not in [];'foo';[]"):
            assert_in("foo", [], "{msg};{first!r};{second!r}")

    # assert_not_in()

    def test_assert_not_in__does_not_contain(self):
        assert_not_in("foo", [])

    def test_assert_not_in__does_contain__default_message(self):
        with _assert_raises_assertion("'foo' is in ['foo', 'bar', 'baz']"):
            assert_not_in("foo", ["foo", "bar", "baz"])

    def test_assert_not_in__does_contain__custom_message(self):
        with _assert_raises_assertion("'foo' is in ['foo', 'bar'];'foo';bar"):
            assert_not_in("foo", ["foo", "bar"], "{msg};{first!r};{second[1]}")

    # assert_count_equal()

    def test_assert_count_equal__equal(self):
        with assert_succeeds(AssertionError):
            assert_count_equal(["a"], ["a"])

    def test_assert_count_equal__equal_differing_types(self):
        with assert_succeeds(AssertionError):
            assert_count_equal(["a"], {"a"})

    def test_assert_count_equal__ignore_order(self):
        with assert_succeeds(AssertionError):
            assert_count_equal(["a", "b"], ["b", "a"])

    def test_assert_count_equal__missing_from_sequence1(self):
        with _assert_raises_assertion("missing from sequence 1: 'a'"):
            assert_count_equal([], {"a"})

    def test_assert_count_equal__multiple_missing_from_sequence1(self):
        with _assert_raises_assertion("missing from sequence 1: 'b', 'c'"):
            assert_count_equal(["a"], ["a", "b", "c"])

    def test_assert_count_equal__respect_duplicates(self):
        with _assert_raises_assertion("missing from sequence 1: 'a'"):
            assert_count_equal({"a"}, ["a", "a"])

    def test_assert_count_equal__missing_from_sequence2(self):
        with _assert_raises_assertion("missing from sequence 2: 'a', 'c'"):
            assert_count_equal(["a", "b", "c"], ["b"])

    def test_assert_count_equal__missing_from_both(self):
        msg = "missing from sequence 1: 'd'; missing from sequence 2: 'b', 'c'"
        with _assert_raises_assertion(msg):
            assert_count_equal(["a", "b", "c"], ["a", "d"])

    def test_assert_count_equal__custom_message(self):
        with _assert_raises_assertion("missing from sequence 1: 'a';[];['a']"):
            assert_count_equal([], ["a"], "{msg};{first};{second}")

    # assert_between()

    def test_assert_between__within_range(self):
        assert_between(0, 10, 0)
        assert_between(0, 10, 10)
        assert_between(0, 10, 5)

    def test_assert_between__too_low__default_message(self):
        with _assert_raises_assertion("-1 is not between 0 and 10"):
            assert_between(0, 10, -1)

    def test_assert_between__too_high__custom_message(self):
        with _assert_raises_assertion("11 is not between 0 and 10;0;10;11"):
            assert_between(0, 10, 11, "{msg};{lower};{upper};{expr}")

    # assert_is_instance()

    def _is_instance_message(self, expr, expected_type, real_type):
        expected_message = "{!r} is an instance of <class {}>, expected {}".format(
            expr, real_type, expected_type
        )
        if sys.version_info[0] < 3:
            return expected_message.replace("class", "type")
        else:
            return expected_message

    def test_assert_is_instance__single_type(self):
        assert_is_instance(4, int)
        assert_is_instance(OSError(), Exception)

    def test_assert_is_instance__multiple_types(self):
        assert_is_instance(4, (str, int))

    def test_assert_is_instance__default_message(self):
        expected_message = self._is_instance_message(
            "my string", "<class 'int'>", "'str'"
        )
        with _assert_raises_assertion(expected_message):
            assert_is_instance("my string", int)

    def test_assert_is_instance__custom_message_single_type(self):
        expected_message = self._is_instance_message(
            "my string", "<class 'int'>", "'str'"
        )
        expected = "{};my string;(<class 'int'>,)".format(expected_message)
        expected = expected.replace("class", self._type_string)
        with _assert_raises_assertion(expected):
            assert_is_instance("my string", int, "{msg};{obj};{types}")

    def test_assert_is_instance__custom_message_multiple_types(self):
        expected_message = self._is_instance_message(
            "my string", "(<class 'int'>, <class 'float'>)", "'str'"
        )
        expected = "{};my string;(<class 'int'>, <class 'float'>)".format(
            expected_message
        )
        expected = expected.replace("class", self._type_string)
        with _assert_raises_assertion(expected):
            assert_is_instance(
                "my string", (int, float), "{msg};{obj};{types}"
            )

    # assert_not_is_instance()

    def _not_is_instance_message(self, obj):
        expected_message = "{!r} is an instance of {}".format(
            obj, obj.__class__
        )
        if sys.version_info[0] < 3:
            expected_message = expected_message.replace("class", "type")
            expected_message = expected_message.replace(
                "type 'OSError'", "type 'exceptions.OSError'"
            )
        return expected_message

    def test_assert_not_is_instance__single_type(self):
        assert_not_is_instance(4, str)

    def test_assert_not_is_instance__multiple_types(self):
        assert_not_is_instance(4, (str, bytes))

    def test_assert_not_is_instance__default_message(self):
        obj = OSError()
        expected_message = self._not_is_instance_message(obj)
        with _assert_raises_assertion(expected_message):
            assert_not_is_instance(obj, Exception)

    def test_assert_not_is_instance__custom_message__single_type(self):
        msg = self._not_is_instance_message("Foo")
        expected = "{};Foo;(<class 'str'>,)".format(msg)
        expected = expected.replace("class", self._type_string)
        with _assert_raises_assertion(expected):
            assert_not_is_instance("Foo", str, "{msg};{obj};{types!r}")

    def test_assert_not_is_instance__custom_message__multiple_types(self):
        msg = self._not_is_instance_message("Foo")
        expected = "{};Foo;(<class 'str'>, <class 'int'>)".format(msg)
        expected = expected.replace("class", self._type_string)
        with _assert_raises_assertion(expected):
            assert_not_is_instance("Foo", (str, int), "{msg};{obj};{types!r}")

    # assert_has_attr()

    def test_assert_has_attr__has_attribute(self):
        d = _DummyObject()
        assert_has_attr(d, "value")

    def test_assert_has_attr__does_not_have_attribute__default_message(self):
        d = _DummyObject()
        with _assert_raises_assertion("<Dummy> does not have attribute 'foo'"):
            assert_has_attr(d, "foo")

    def test_assert_has_attr__does_not_have_attribute__custom_message(self):
        d = _DummyObject()
        expected = "<Dummy> does not have attribute 'foo';<Dummy>;foo"
        with _assert_raises_assertion(expected):
            assert_has_attr(d, "foo", msg_fmt="{msg};{obj!r};{attribute}")

    # assert_datetime_about_now()

    def test_assert_datetime_about_now__close(self):
        assert_datetime_about_now(datetime.now())

    def test_assert_datetime_about_now__none__default_message(self):
        expected_message = r"^None is not a valid date/time$"
        with assert_raises_regex(AssertionError, expected_message):
            assert_datetime_about_now(None)

    def test_assert_datetime_about_now__none__custom_message(self):
        dt = datetime.now().date().isoformat()
        expected = "None is not a valid date/time;None;{}".format(dt)
        with _assert_raises_assertion(expected):
            assert_datetime_about_now(
                None, msg_fmt="{msg};{actual!r};{now:%Y-%m-%d}"
            )

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
        expected_message = (
            r"^datetime.datetime\(1990, 4, 13, 12, 30, 15\) "
            "is not close to current date/time$"
        )
        with assert_raises_regex(AssertionError, expected_message):
            assert_datetime_about_now(then)

    def test_assert_datetime_about_now__custom_message(self):
        then = datetime(1990, 4, 13, 12, 30, 15)
        now = datetime.now().date().isoformat()
        expected = (
            "datetime.datetime(1990, 4, 13, 12, 30, 15) "
            "is not close to current date/time;12:30;{}".format(now)
        )
        with _assert_raises_assertion(expected):
            assert_datetime_about_now(
                then, msg_fmt="{msg};{actual:%H:%M};{now:%Y-%m-%d}"
            )

    # assert_datetime_about_now_utc()

    def test_assert_datetime_about_now_utc__close(self):
        assert_datetime_about_now_utc(datetime.utcnow())

    def test_assert_datetime_about_now_utc__none__default_message(self):
        expected_message = r"^None is not a valid date/time$"
        with assert_raises_regex(AssertionError, expected_message):
            assert_datetime_about_now_utc(None)

    def test_assert_datetime_about_now_utc__none__custom_message(self):
        dt = datetime.utcnow().date().isoformat()
        expected = "None is not a valid date/time;None;{}".format(dt)
        with _assert_raises_assertion(expected):
            assert_datetime_about_now_utc(
                None, msg_fmt="{msg};{actual!r};{now:%Y-%m-%d}"
            )

    def test_assert_datetime_about_now_utc__too_low(self):
        then = datetime.utcnow() - timedelta(minutes=1)
        with assert_raises(AssertionError):
            assert_datetime_about_now_utc(then)

    def test_assert_datetime_about_now_utc__too_high(self):
        then = datetime.utcnow() + timedelta(minutes=1)
        with assert_raises(AssertionError):
            assert_datetime_about_now_utc(then)

    def test_assert_datetime_about_now_utc__default_message(self):
        then = datetime(1990, 4, 13, 12, 30, 15)
        expected_message = (
            r"datetime.datetime\(1990, 4, 13, 12, 30, 15\) "
            r"is not close to current UTC date/time$"
        )
        with assert_raises_regex(AssertionError, expected_message):
            assert_datetime_about_now_utc(then)

    def test_assert_datetime_about_now_utc__custom_message(self):
        then = datetime(1990, 4, 13, 12, 30, 15)
        now = datetime.utcnow().date().isoformat()
        expected = (
            "datetime.datetime(1990, 4, 13, 12, 30, 15) "
            "is not close to current UTC date/time;12:30;{}".format(now)
        )
        with _assert_raises_assertion(expected):
            assert_datetime_about_now_utc(
                then, msg_fmt="{msg};{actual:%H:%M};{now:%Y-%m-%d}"
            )

    # assert_raises()

    def test_assert_raises__raises_right_exception(self):
        with assert_raises(KeyError):
            raise KeyError()

    def test_assert_raises__exc_val(self):
        exc = KeyError()
        with assert_raises(KeyError) as context:
            raise exc
        assert_is(exc, context.exc_val)

    def test_assert_raises__exc_val_within_context(self):
        with assert_raises(RuntimeError):
            with assert_raises(KeyError) as context:
                context.exc_val

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
        expected = "KeyError not raised;KeyError;KeyError"
        with _assert_raises_assertion(expected):
            with assert_raises(
                KeyError, msg_fmt="{msg};{exc_type.__name__};{exc_name}"
            ):
                pass

    def test_assert_raises__wrong_exception_raised(self):
        try:
            with assert_raises(IndexError):
                raise KeyError()
        except KeyError:
            pass
        except Exception as exc:
            fail(str(exc) + " was raised")
        else:
            fail("no exception raised")

    def test_assert_raises__add_test_called(self):
        called = Box(False)

        def extra_test(exc):
            assert_is_instance(exc, KeyError)
            called.value = True

        with assert_raises(KeyError) as context:
            context.add_test(extra_test)
            raise KeyError()
        assert_true(called.value, "extra_test() was not called")

    def test_assert_raises__add_test_not_called(self):
        called = Box(False)

        def extra_test(_):
            called.value = True

        with assert_raises(AssertionError):
            with assert_raises(KeyError) as context:
                context.add_test(extra_test)
        assert_false(called.value, "extra_test() was unexpectedly called")

    # assert_raises_regex()

    def test_assert_raises_regex__raises_right_exception(self):
        with assert_raises_regex(KeyError, r"test.*"):
            raise KeyError("test message")

    def test_assert_raises_regex__raises_right_exception__compiled(self):
        with assert_raises_regex(KeyError, re.compile(r"test.*")):
            raise KeyError("test message")

    def test_assert_raises_regex__exception_not_raised__default_message(self):
        with _assert_raises_assertion("KeyError not raised"):
            with assert_raises_regex(KeyError, r"test"):
                pass

    def test_assert_raises_regex__exception_not_raised__custom_message(self):
        expected = "KeyError not raised;KeyError;KeyError;'';test"
        with _assert_raises_assertion(expected):
            msg_fmt = "{msg};{exc_type.__name__};{exc_name};{text!r};{pattern}"
            with assert_raises_regex(KeyError, r"test", msg_fmt=msg_fmt):
                pass

    def test_assert_raises_regex__no_message__default_message(self):
        with _assert_raises_assertion("KeyError without message"):
            with assert_raises_regex(KeyError, r"test"):
                raise KeyError()

    def test_assert_raises_regex__no_message__custom_message(self):
        expected = "KeyError without message;KeyError;KeyError;None;test"
        with _assert_raises_assertion(expected):
            msg_fmt = "{msg};{exc_type.__name__};{exc_name};{text!r};{pattern}"
            with assert_raises_regex(KeyError, r"test", msg_fmt=msg_fmt):
                raise KeyError()

    def test_assert_raises_regex__wrong_exception_raised(self):
        try:
            with assert_raises_regex(IndexError, "test message"):
                raise KeyError("test message")
        except KeyError:
            pass
        except Exception as exc:
            fail(str(exc) + " was raised")
        else:
            fail("no exception raised")

    def test_assert_raises_regex__wrong_error__default_message(self):
        with _assert_raises_assertion("'wrong message' does not match 'test'"):
            with assert_raises_regex(KeyError, r"test"):
                raise KeyError("wrong message")

    def test_assert_raises_regex__wrong_error__pattern_default_message(self):
        with _assert_raises_assertion("'wrong message' does not match 'test'"):
            with assert_raises_regex(KeyError, re.compile(r"test")):
                raise KeyError("wrong message")

    def test_assert_raises_regex__wrong_error__custom_message(self):
        expected = (
            "'wrong message' does not match 'test';KeyError;KeyError;"
            "'wrong message';test"
        )
        with _assert_raises_assertion(expected):
            msg_fmt = "{msg};{exc_type.__name__};{exc_name};{text!r};{pattern}"
            with assert_raises_regex(KeyError, r"test", msg_fmt=msg_fmt):
                raise KeyError("wrong message")

    # assert_raises_errno()

    def test_assert_raises_errno__right_errno(self):
        with assert_raises_errno(OSError, 20):
            raise OSError(20, "Test error")

    def test_assert_raises_errno__no_exception_raised__default_message(self):
        with _assert_raises_assertion("OSError not raised"):
            with assert_raises_errno(OSError, 20):
                pass

    def test_assert_raises_errno__no_exception_raised__custom_message(self):
        expected = "OSError not raised;OSError;OSError;20;None"
        with _assert_raises_assertion(expected):
            msg_fmt = (
                "{msg};{exc_type.__name__};{exc_name};{expected_errno};"
                "{actual_errno}"
            )
            with assert_raises_errno(OSError, 20, msg_fmt=msg_fmt):
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
        expected = "wrong errno: 20 != 1;OSError;OSError;20;1"
        with _assert_raises_assertion(expected):
            msg_fmt = (
                "{msg};{exc_type.__name__};{exc_name};{expected_errno};"
                "{actual_errno}"
            )
            with assert_raises_errno(OSError, 20, msg_fmt=msg_fmt):
                raise OSError(1, "Test error")

    # assert_succeeds()

    def test_assert_succeeds__no_exception_raised(self):
        with assert_succeeds(KeyError):
            pass

    def test_assert_succeeds__expected_exception__default_message(self):
        with _assert_raises_assertion("KeyError was unexpectedly raised"):
            with assert_succeeds(KeyError):
                raise KeyError()

    def test_assert_succeeds__expected_exception__custom_message(self):
        expected = (
            "KeyError was unexpectedly raised;KeyError;KeyError;test error"
        )
        with _assert_raises_assertion(expected):
            msg_fmt = (
                "{msg};{exc_type.__name__};{exc_name};{exception.args[0]}"
            )
            with assert_succeeds(KeyError, msg_fmt=msg_fmt):
                raise KeyError("test error")

    def test_assert_succeeds__unexpected_exception(self):
        try:
            with assert_succeeds(ValueError):
                raise KeyError()
        except KeyError:
            pass
        else:
            raise AssertionError("KeyError was not raised")

    # assert_warns()

    def test_assert_warns__default_message(self):
        with assert_raises_regex(AssertionError, r"^ImportWarning not issued"):
            with assert_warns(ImportWarning):
                pass

    def test_assert_warns__custom_message(self):
        exception = "ImportWarning not issued;ImportWarning;ImportWarning"
        with _assert_raises_assertion(exception):
            msg_fmt = "{msg};{exc_type.__name__};{exc_name}"
            with assert_warns(ImportWarning, msg_fmt=msg_fmt):
                pass

    def test_assert_warns__warned(self):
        with assert_succeeds(AssertionError):
            with assert_warns(FutureWarning):
                warn("foo", FutureWarning)

    def test_assert_warns__not_warned(self):
        with assert_raises(AssertionError):
            with assert_warns(ImportWarning):
                pass

    def test_assert_warns__wrong_type(self):
        with assert_raises(AssertionError):
            with assert_warns(ImportWarning):
                warn("foo", UnicodeWarning)

    def test_assert_warns__multiple_warnings(self):
        with assert_succeeds(AssertionError):
            with assert_warns(UserWarning):
                warn("foo", UnicodeWarning)
                warn("bar", UserWarning)
                warn("baz", FutureWarning)

    def test_assert_warns__warning_handler_deinstalled_on_success(self):
        with catch_warnings(record=True) as warnings:
            with assert_warns(UserWarning):
                warn("foo", UserWarning)
            assert warnings is not None
            assert_equal(0, len(warnings))
            warn("bar", UserWarning)
            assert_equal(1, len(warnings))

    def test_assert_warns__warning_handler_deinstalled_on_failure(self):
        with catch_warnings(record=True) as warnings:
            try:
                with assert_warns(UserWarning):
                    pass
            except AssertionError:
                pass
            assert warnings is not None
            assert_equal(0, len(warnings))
            warn("bar", UserWarning)
            assert_equal(1, len(warnings))

    def test_assert_warns__add_test_called(self):
        called = Box(False)

        def extra_test(warning):
            assert_is(warning.category, UserWarning)
            called.value = True
            return True

        with assert_warns(UserWarning) as context:
            context.add_test(extra_test)
            warn("bar", UserWarning)
        assert_true(called.value, "extra_test() was not called")

    def test_assert_warns__add_test_not_called(self):
        called = Box(False)

        def extra_test(_):
            called.value = True

        with assert_raises(AssertionError):
            with assert_warns(UserWarning) as context:
                context.add_test(extra_test)
        assert_false(called.value, "extra_test() was unexpectedly called")

    # assert_warns_regex()

    def test_assert_warns_regex__warned(self):
        with assert_succeeds(AssertionError):
            with assert_warns_regex(FutureWarning, r"fo+"):
                warn("foo", FutureWarning)

    def test_assert_warns_regex__warning_text_matches_in_the_middle(self):
        with assert_succeeds(AssertionError):
            with assert_warns_regex(FutureWarning, r"o"):
                warn("foo", FutureWarning)

    def test_assert_warns_regex__not_warned(self):
        with assert_raises(AssertionError):
            with assert_warns_regex(UserWarning, r"foo"):
                pass

    def test_assert_warns_regex__wrong_type(self):
        with assert_raises(AssertionError):
            with assert_warns_regex(ImportWarning, r"foo"):
                warn("foo", UnicodeWarning)

    def test_assert_warns_regex__wrong_message(self):
        with assert_raises(AssertionError):
            with assert_warns_regex(UnicodeWarning, r"foo"):
                warn("bar", UnicodeWarning)

    def test_assert_warns_regex__multiple_warnings(self):
        with assert_succeeds(AssertionError):
            with assert_warns_regex(UserWarning, r"bar2"):
                warn("foo", UnicodeWarning)
                warn("bar1", UserWarning)
                warn("bar2", UserWarning)
                warn("bar3", UserWarning)
                warn("baz", FutureWarning)

    def test_assert_warns_regex__warning_handler_deinstalled_on_success(self):
        with catch_warnings(record=True) as warnings:
            with assert_warns_regex(UserWarning, r"foo"):
                warn("foo", UserWarning)
            assert warnings is not None
            assert_equal(0, len(warnings))
            warn("bar", UserWarning)
            assert_equal(1, len(warnings))

    def test_assert_warns_regex__warning_handler_deinstalled_on_failure(self):
        with catch_warnings(record=True) as warnings:
            try:
                with assert_warns_regex(UserWarning, r""):
                    pass
            except AssertionError:
                pass
            assert warnings is not None
            assert_equal(0, len(warnings))
            warn("bar", UserWarning)
            assert_equal(1, len(warnings))

    def test_assert_warns_regex__not_issued__default_message(self):
        with _assert_raises_assertion(
            "no UserWarning matching 'foo.*bar' issued"
        ):
            with assert_warns_regex(UserWarning, r"foo.*bar"):
                pass

    def test_assert_warns_regex__not_issued__custom_message(self):
        expected = (
            "no ImportWarning matching 'abc' issued;ImportWarning;"
            "ImportWarning;abc"
        )
        with _assert_raises_assertion(expected):
            msg_fmt = "{msg};{exc_type.__name__};{exc_name};{pattern}"
            with assert_warns_regex(ImportWarning, r"abc", msg_fmt=msg_fmt):
                pass

    def test_assert_warns_regex__wrong_message__default_message(self):
        with _assert_raises_assertion(
            "no UserWarning matching 'foo.*bar' issued"
        ):
            with assert_warns_regex(UserWarning, r"foo.*bar"):
                pass

    def test_assert_warns_regex__wrong_message__custom_message(self):
        expected = (
            "no UserWarning matching 'foo.*bar' issued;UserWarning;"
            "UserWarning;foo.*bar"
        )
        with _assert_raises_assertion(expected):
            msg_fmt = "{msg};{exc_type.__name__};{exc_name};{pattern}"
            with assert_warns_regex(UserWarning, r"foo.*bar", msg_fmt=msg_fmt):
                pass

    # assert_json_subset()

    def test_assert_json_subset__different_types(self):
        with _assert_raises_assertion("element $ differs: {} != []"):
            assert_json_subset({}, [])

    def test_assert_json_subset__empty_objects(self):
        with assert_succeeds(AssertionError):
            assert_json_subset({}, {})

    def test_assert_json_subset__objects_equal(self):
        with assert_succeeds(AssertionError):
            assert_json_subset(
                {"foo": 3, "bar": "abc"}, {"bar": "abc", "foo": 3}
            )

    def test_assert_json_subset__one_key_missing_from_first_object(self):
        with assert_succeeds(AssertionError):
            assert_json_subset({"foo": 3}, {"foo": 3, "bar": 3})

    def test_assert_json_subset__one_key_missing_from_second_object(self):
        with _assert_raises_assertion("element 'bar' missing from element $"):
            assert_json_subset({"foo": 3, "bar": 3}, {"foo": 3})

    def test_assert_json_subset__multiple_keys_missing_from_second_object(
        self
    ):
        with _assert_raises_assertion(
            "elements 'bar', 'baz', and 'foo' missing from element $"
        ):
            assert_json_subset({"foo": 3, "bar": 3, "baz": 3}, {})

    def test_assert_json_subset__value_differs(self):
        with _assert_raises_assertion("element $['foo'] differs: 3 != 4"):
            assert_json_subset({"foo": 3}, {"foo": 4})

    def test_assert_json_subset__empty_lists(self):
        with assert_succeeds(AssertionError):
            assert_json_subset([], [])

    def test_assert_json_subset__different_sized_lists(self):
        with _assert_raises_assertion("JSON array $ differs in size: 2 != 1"):
            assert_json_subset([1, 2], [1])
        with _assert_raises_assertion("JSON array $ differs in size: 1 != 2"):
            assert_json_subset([1], [1, 2])

    def test_assert_json_subset__different_list_values(self):
        with _assert_raises_assertion("element $[0] differs: {} != []"):
            assert_json_subset([{}], [[]])

    def test_assert_json_subset__fundamental_types_differ(self):
        with _assert_raises_assertion("element $[0] differs: 1 != 'foo'"):
            assert_json_subset([1], ["foo"])

    def test_assert_json_subset__fundamental_values_differ(self):
        with _assert_raises_assertion("element $[0] differs: 'bar' != 'foo'"):
            assert_json_subset(["bar"], ["foo"])

    def test_assert_json_subset__none(self):
        with assert_succeeds(AssertionError):
            assert_json_subset([None], [None])
        with _assert_raises_assertion("element $[0] differs: 42 != None"):
            assert_json_subset([42], [None])
        with _assert_raises_assertion("element $[0] differs: None != 42"):
            assert_json_subset([None], [42])

    def test_assert_json_subset__compare_int_and_float(self):
        with assert_succeeds(AssertionError):
            assert_json_subset([42], [42.0])
            assert_json_subset([42.0], [42])

    def test_assert_json_subset__unsupported_type(self):
        msg = "unsupported type <{} 'set'>".format(self._type_string)
        with assert_raises_regex(TypeError, msg):
            assert_json_subset([set()], [set()])

    def test_assert_json_subset__subtypes(self):
        with assert_succeeds(AssertionError):
            assert_json_subset(OrderedDict(), {})
            assert_json_subset({}, OrderedDict())

    def test_assert_json_subset__second_is_string(self):
        with assert_succeeds(AssertionError):
            assert_json_subset({}, "{  }")

    def test_assert_json_subset__second_is_unsupported_json_string(self):
        msg = "second must decode to dict or list, not <{} 'int'>".format(
            self._type_string
        )
        with _assert_raises_assertion(msg):
            assert_json_subset({}, "42")

    def test_assert_json_subset__second_is_invalid_json_string(self):
        try:
            from json import JSONDecodeError
        except ImportError:
            JSONDecodeError = ValueError  # type: ignore
        with assert_raises(JSONDecodeError):
            assert_json_subset({}, ",")

    def test_assert_json_subset__second_is_bytes(self):
        with assert_succeeds(AssertionError):
            assert_json_subset([u"föo"], u'["föo"]'.encode("utf-8"))

    def test_assert_json_subset__second_is_latin1_bytes(self):
        with assert_raises(UnicodeDecodeError):
            assert_json_subset([u"föo"], u'["föo"]'.encode("iso-8859-1"))

    def test_assert_json_subset__invalid_type(self):
        with assert_raises_regex(
            TypeError, "second must be dict, list, str, or bytes"
        ):
            assert_json_subset({}, 42)  # type: ignore
