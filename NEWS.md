## News in asserts 0.11.0

### API-Incompatible Changes

* Drop support for Python 2.7 and 3.5.

## News in asserts 0.10.0

### API-Incompatible Changes

* Drop support for Python 3.4.

### API Additions

* `AssertRaisesContext` and `AssertWarnsContext` now return themselves
  when `__enter__()` is called. By extension it now easier to call
  `add_test()` with `assert_raises()` et al:

```python
with assert_raises(KeyError) as context:
    context.add_test(...)
    ...
```  

* Add `AssertRaisesContext.exc_val` property to access the caught
  exception after leaving the context manager:

```python
with assert_raises(KeyError) as context:
    ...
assert_equal("expected message", str(context.exc_val))
```  

## News in asserts 0.9.1

### Improvements

* `AssertRaisesContext` and sub-classes are now generic over the
  exception type.

## News in asserts 0.9.0

### API Additions

* Add `assert_json_subset()`.

## News in asserts 0.8.6

### Improvements

* Add support for Python 3.7 (contributed by Frank Niessink).

## News in asserts 0.8.5

### API Additions

* Add `assert_dict_equal()`.
* Add `assert_dict_superset()`.

### Improvements

* `assert_equal()`: Use `assert_dict_equal()` if applicable.

## News in asserts 0.8.4

### Improvements

* `fail()` is now marked with `NoReturn` in type stub.

### Bug Fixes

* Improve type annotations for Python 2.

## News in asserts 0.8.3

### Bug Fixes

* Fix type signature of `AssertRaisesContext.__exit__()`.

## News in asserts 0.8.2

### Improvements

* Add a py.typed file to signal that this package supports type hints.

## News in asserts 0.8.1

### Bug Fixes

* `assert_raises_regex()`: Handle exceptions without any message correctly.

## News in asserts 0.8.0

### API-Incompatible Changes

* Replace `msg` argument with `msg_fmt` in all assertions (except `fail()`).
  This allows you to customize error messages more easily than before, because
  `format()` with appropriate keyword arguments is now called on these
  strings. See the documentation of individual assertions for the supported
  arguments.
* Replace AssertRaisesContext.msg and AssertWarnsContext.msg with msg_fmt.
* assert_almost_equal(), assert_not_almost_equal(): Place msg_fmt as third
  argument.

### API Additions

* assert_count_equal(): Add `msg_fmt` argument.
* Add AssertRaisesErrnoContext, AssertRaisesRegexContext, and
  AssertWarnsRegexContext.

## News in asserts 0.7.3

### API Additions

* Add assert_not_almost_equal().

### Improvements

* assert_almost_equal(): Raise ValueError if diff <= 0.

### Bug Fixes

* assert_almost_equal() would never fail if a delta was supplied and the
  second number was smaller than the first.
* Use fail() instead of raise AssertionError in a few assertions.

## News in asserts 0.7.2

### API Additions

* Add assert_warns() and assert_warns_regex().

## News in asserts 0.7.1

* Distribute as wheel.
* asserts is now a package, instead of a module.

## News in asserts 0.7.0

* Add a stub file.

### API Additions

* Add assert_count_equal().

## News in asserts 0.6

### API Additions

* Add assert_less(), assert_less_equal(), assert_greater(), and
  assert_greater_equal().
* Add assert_not_is_instance().

### Improvements

* assert_datetime_about_now()/assert_datetime_about_now_utc(): Handle
  comparison with None more gracefully.

## News in asserts 0.5.1

* Add the LICENSE file to the distribution.

## News in asserts 0.5

Initial release.
