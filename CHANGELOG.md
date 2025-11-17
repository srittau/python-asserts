# Changelog for python-asserts

python-asserts adheres to [semantic versioning](https://semver.org/).

## UNRELEASED –

### Added

- Add support for Python 3.13 and 3.14.
- Add `assert_datetime_now()`.

### Changed

- Fail with `AssertionError`, not `TypeError`, if a timezone-aware datetime is
  passed to `assert_datetime_about_now()` or `assert_datetime_about_now_utc()`.
- Modernize type annotations.

### Removed

- Drop support for Python 3.8 and 3.9.

## [0.13.1] – 2024-04-29

### Fixed

Fixed Python 3.12 deprecation warnings.

## [0.13.0] – 2024-03-13

### Added

- Add support for Python 3.12.
- Add `Present` and `Absent` for absence checks in `assert_json_subset()`.

### Removed

- Drop support for Python 3.7.

### Deprecated

- Deprecate `Exists` in favor of `Present` and `Absent` in
  `assert_json_subset()`.

## [0.12.0]

### Added

- Add `assert_not_regex()`.

### Changed

- Modernize the type stubs.

### Removed

- Drop support for Python 3.6.

## [0.11.1]

### Added

- `assert_json_subset()` can now check for the existence or non-existence
  of object members using the new `Exists` helper.
- Non-string (or `Exists`) object member names in the first argument to
  `assert_json_subset()` now raise a `TypeError`.

## [0.11.0]

### Removed

- Drop support for Python 2.7 and 3.5.

## [0.10.0]

### Added

- `AssertRaisesContext` and `AssertWarnsContext` now return themselves
  when `__enter__()` is called. By extension it now easier to call
  `add_test()` with `assert_raises()` et al:

```python
with assert_raises(KeyError) as context:
    context.add_test(...)
    ...
```

- Add `AssertRaisesContext.exc_val` property to access the caught
  exception after leaving the context manager:

```python
with assert_raises(KeyError) as context:
    ...
assert_equal("expected message", str(context.exc_val))
```

### Removed

- Drop support for Python 3.4.

## [0.9.1]

### Changed

- `AssertRaisesContext` and sub-classes are now generic over the
  exception type.

## [0.9.0]

### Added

- Add `assert_json_subset()`.

## [0.8.6]

### Added

- Add support for Python 3.7 (contributed by Frank Niessink).

## [0.8.5]

### Added

- Add `assert_dict_equal()`.
- Add `assert_dict_superset()`.

### Changed

- `assert_equal()`: Use `assert_dict_equal()` if applicable.

## [0.8.4]

### Changed

- `fail()` is now marked with `NoReturn` in type stub.

### Fixed

- Improve type annotations for Python 2.

## [0.8.3]

### Fixed

- Fix type signature of `AssertRaisesContext.__exit__()`.

## [0.8.2]

### Added

- Add a py.typed file to signal that this package supports type hints.

## [0.8.1]

### Fixed

- `assert_raises_regex()`: Handle exceptions without any message correctly.

## [0.8.0]

### Added

- assert_count_equal(): Add `msg_fmt` argument.
- Add AssertRaisesErrnoContext, AssertRaisesRegexContext, and
  AssertWarnsRegexContext.

### Changed

- Replace `msg` argument with `msg_fmt` in all assertions (except `fail()`).
  This allows you to customize error messages more easily than before, because
  `format()` with appropriate keyword arguments is now called on these
  strings. See the documentation of individual assertions for the supported
  arguments.
- Replace AssertRaisesContext.msg and AssertWarnsContext.msg with msg_fmt.
- assert_almost_equal(), assert_not_almost_equal(): Place msg_fmt as third
  argument.

## [0.7.3]

### Added

- Add assert_not_almost_equal().

### Changed

- assert_almost_equal(): Raise ValueError if diff <= 0.

### Fixed

- assert_almost_equal() would never fail if a delta was supplied and the
  second number was smaller than the first.
- Use fail() instead of raise AssertionError in a few assertions.

## [0.7.2]

### Added

- Add assert_warns() and assert_warns_regex().

## [0.7.1]

### Changed

- Distribute a wheel.
- asserts is now a package, instead of a module.

## [0.7.0]

### Added

- Add a stub file.
- Add assert_count_equal().

## [0.6]

### Added

- Add assert_less(), assert_less_equal(), assert_greater(), and
  assert_greater_equal().
- Add assert_not_is_instance().

### Changed

- assert_datetime_about_now()/assert_datetime_about_now_utc(): Handle
  comparison with None more gracefully.

## [0.5.1]

### Added

- Add the LICENSE file to the distribution.

## [0.5]

Initial release.
