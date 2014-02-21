* richer assertion messages, especially for assert_equal
* better Docstrings
* Doctests
* missing assertions:
    * assert_not_is_instance
    * assert_warns
    * assert_warns_regex
    * assert_not_almost_equal
    * assert_greater
    * assert_greater_equal
    * assert_less
    * assert_less_equal
    * assert_not_regex
    * assert_count_equal
* assert_almost_equal: add delta argument
* unit test cleanup and completion: for every assertion, there should be at
  least three tests: test success, test failure with default message, test
  failure with custom message
