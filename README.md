Python Asserts
==============

Rich Assertions for Python

This package provides a few advantages over the assertions provided by
unittest.TestCase:

* Can be used stand-alone, for example:
    * In test cases, not derived from TestCase.
    * In fake and mock classes.
    * In implementations as rich alternative to the assert statement.
* PEP 8 compliance.
* Custom stand-alone assertions can be written easily.
* Arguably a better separation of concerns, since TestCase is responsible
  for test running only, if assertion functions are used exclusively.

There are a few regressions compared to assertions from TestCase:

* The default assertion class (AssertionError) can not be overwritten. This
  is rarely a problem in practice.
* asserts does not support the addTypeEqualityFunc() functionality.


Usage:

```python
from asserts import assert_true, assert_equal, assert_raises

my_var = 13
assert_equal(13, my_var)
assert_true(True, msg="custom failure message")
with assert_raises(KeyError):
    raise KeyError()
```
